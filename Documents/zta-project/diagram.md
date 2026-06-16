<pre>
sequenceDiagram
    autonumber
    actor User as User (Browser)
    participant ModHeader as ModHeader (Device Check)
    participant PEP as Policy Enforcement Point<br/>(OAuth2 Proxy @ :4180)
    participant IdP as Identity Provider<br/>(GitHub OAuth)
    participant App as Upstream Application<br/>(Nginx App @ :80)
    
    note over User, PEP: Phase 1: Authentication (Identity Check)
    User->>+PEP: Request http://localhost:4180
    
    alt is authenticated (valid cookie)
        PEP-->>User: Proceed (Status 200)
    else is NOT authenticated (invalid/no cookie)
        PEP-->>-User: Redirect to IdP (Status 302/403)
        User->>IdP: Login & Authorize App
        IdP-->>User: Redirect to Callback w/ Code
        User->>+PEP: GET /oauth2/callback
        PEP->>PEP: Exchange Code for Token
        PEP->>PEP: Set _oauth2_proxy Cookie
        PEP-->>-User: Redirect to Home (/) w/ Cookie
        note right of PEP: Identity Verified
    end

    note over User, App: Phase 2: Authorization (Device Check)
    note right of ModHeader: Requires 'X-Device-ID: Asset-12345' header
    User->>+PEP: Request w/ Cookie
    
    opt ModHeader is active
        PEP->>App: Forward Request + Headers
        
        alt Header is valid
            App-->>User: Sensitive Internal Dashboard
            note right of User: Successful Entry
        else Header is missing/invalid
            App-->>User: Forbidden (Device Check Failure)
            note right of User: Device Denied
        end
    end
    deactivate App
    deactivate PEP
</pre>
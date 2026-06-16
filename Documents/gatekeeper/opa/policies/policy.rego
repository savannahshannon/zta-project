package authentik.authz

import future.keywords.if

# Default to denying access
default allow = false

# RULE 1: Admin Bypass (Emergency Access)
# If the user is 'akadmin', let them in regardless of time/IP
allow if {
    input.user.username == "akadmin"
}

# RULE 2: The "Phase 1" Requirements for everyone else
# This satisfies the "GitHub + CIDR + Business Hours" requirement
allow if {
    # Only applies to external (GitHub/Google) users
    input.user.type == "external"

    # 1. Business Hours (9 AM to 10 PM)
    input.context.time.hour >= 9
    input.context.time.hour <= 22

    # 2. CIDR Range (University VPN / Localhost)
    # We include 172.16.0.0/12 to cover Docker's internal networking
    is_trusted_network
}

is_trusted_network if {
    net.cidr_contains("127.0.0.0/8", input.context.http_client_ip)
}

is_trusted_network if {
    net.cidr_contains("172.16.0.0/12", input.context.http_client_ip)
}
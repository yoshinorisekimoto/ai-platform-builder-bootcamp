### Information Boundaries

**Minimum Required Information** (must include)
- Partner ID
- Production endpoint
- current traffic
- expected peak traffic
- peak calculation basis
- recent 429 count
- recent 429 time window

**Prohibited Standard Fields** (must exclude by default)
- end-user IP address
- user ID
- full request payload
- full raw logs

**Exception Approval Conditions** (required to override an exclusion)
- specific technical purpose
- minimum required fields and scope
- relevant time range
- access controls
- retention period
- explicit Data Privacy Owner approval

Approval applies only to the documented fields, purpose, time range, access controls, and retention period.
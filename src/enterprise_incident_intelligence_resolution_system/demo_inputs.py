"""Realistic demo scenario for executive presentations."""

INCIDENT_TICKET = """
INCIDENT ID: INC-2026-0847
TITLE: Customer Portal returning HTTP 503 — widespread login failures
REPORTED BY: NOC Tier-1 (PagerDuty alert P1-CRITICAL)
OPENED: 2026-06-29T08:14:22Z
STATUS: Active — customer-facing degradation

SUMMARY:
Since 08:02 UTC, the Northwind Financial customer portal (portal.northwind-financial.com)
is returning HTTP 503 errors for ~68% of login and account-summary requests. Mobile app
API calls are failing with the same backend errors. Internal admin dashboards show
elevated 5xx rates on the API gateway.

INITIAL SYMPTOMS:
- Spike in 503 responses on /api/v2/auth/login and /api/v2/accounts/summary
- Customer support queue +340% vs. baseline (est. 1,200 callers waiting at peak)
- Payment submission success rate dropped from 99.2% to 41%
- No recent production deployments in the last 6 hours

ESCALATION:
P1 declared at 08:18 UTC. Incident bridge opened. CTO notified per financial-services SLA policy.
""".strip()

AFFECTED_SYSTEMS = """
PRIMARY:
- customer-portal-api (Kubernetes, us-east-1, 24 pods)
- auth-service (OAuth2 / session management)
- account-summary-service (read-heavy PostgreSQL queries)

DATA LAYER:
- postgres-primary-prod (RDS PostgreSQL 15, db.r6g.2xlarge)
- pgbouncer-prod (connection pooler, max 400 connections)

INFRASTRUCTURE:
- api-gateway-prod (Kong, rate limiting enabled)
- redis-session-cache (ElastiCache)

DEPENDENCIES:
- external-fraud-scoring-api (third-party, latency elevated +800ms since 07:55 UTC)
- email-notification-service (degraded, non-blocking)

BLAST RADIUS:
All retail banking customers in US-East region (~2.1M active accounts).
Mobile iOS/Android apps share the same API backend.
""".strip()

LOG_DATA = """
[2026-06-29T08:02:11Z] ERROR auth-service pod/auth-7f3a2 | HikariPool-1 - Connection is not available, request timed out after 30000ms
[2026-06-29T08:02:14Z] ERROR account-summary-service | org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved for roles with the SUPERUSER attribute
[2026-06-29T08:02:19Z] WARN  pgbouncer-prod | pool 'northwind_app' - too many connections (398/400 active)
[2026-06-29T08:03:02Z] ERROR api-gateway | upstream auth-service responded 503 in 30112ms trace_id=8f2c91a0
[2026-06-29T08:04:47Z] ERROR postgres-primary-prod | duration: 28491.231 ms  statement: SELECT a.*, t.balance FROM accounts a JOIN transactions t ON a.id = t.account_id WHERE a.customer_id = $1 ORDER BY t.posted_at DESC LIMIT 500
[2026-06-29T08:05:01Z] ERROR postgres-primary-prod | canceling statement due to statement timeout
[2026-06-29T08:06:33Z] WARN  fraud-scoring-api client | timeout after 10000ms — circuit half-open, 12 retries in 90s
[2026-06-29T08:08:15Z] INFO  on-call-dba | active_connections=412 max_connections=400 — manual intervention started
[2026-06-29T08:09:22Z] ERROR auth-service | java.sql.SQLTransientConnectionException: Connection pool exhausted — 0 idle connections
[2026-06-29T08:11:40Z] WARN  customer-portal-api | thread pool queue depth 890/500 — rejecting new requests
[2026-06-29T08:14:05Z] INFO  incident-bridge | P1 declared — bridge ID BR-2026-0847
[2026-06-29T08:16:18Z] INFO  on-call-dba | terminated PID 1849201 (long-running SELECT, runtime 47m, user app_readonly)
[2026-06-29T08:18:44Z] INFO  pgbouncer-prod | pool utilization dropped to 312/400 after query termination
[2026-06-29T08:22:10Z] INFO  api-gateway | 503 rate decreasing — 68% -> 41%
[2026-06-29T08:25:00Z] INFO  auth-service | connection pool recovering — 18 idle connections available
""".strip()

BUSINESS_CONTEXT = """
ORGANIZATION: Northwind Financial (regional retail bank, $48B AUM)
CUSTOMERS AFFECTED: ~2.1M active accounts (US-East primary market)
REVENUE AT RISK: ~$180K/hour in payment processing fees during peak degradation
SLA COMMITMENTS:
  - Retail portal availability: 99.95% monthly (current breach risk: 0.12% monthly budget consumed in 23 minutes)
  - Payment processing: 99.9% success rate (currently 41% — active SLA breach)
REGULATORY: OCC notification required if customer-facing outage exceeds 30 minutes for core banking services
REPUTATION: Q2 customer NPS target 42 — major outage threatens quarterly target
QUARTERLY CONTEXT: Board review scheduled July 15 — operational resilience is a standing agenda item
""".strip()

DEMO_INPUTS = {
    "incident_ticket": INCIDENT_TICKET,
    "affected_systems": AFFECTED_SYSTEMS,
    "log_data": LOG_DATA,
    "business_context": BUSINESS_CONTEXT,
}

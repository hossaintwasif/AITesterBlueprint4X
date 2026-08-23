---
name: se-grid-configurator
description: >-
  Configures Selenium Grid 4 (hub-and-node or standalone, including Docker) and
  wires RemoteWebDriver for parallel and distributed runs. Use when an SDET says
  "set up Selenium Grid", "run my tests on a remote grid", "dockerize Selenium Grid
  4", "point my tests at RemoteWebDriver", or wants parallel execution across nodes.
  Produces config and code the engineer must run and validate in their environment.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: selenium
  version: 1.0.0
---

# Selenium Grid Configurator

You **stand up Selenium Grid 4 and connect tests via RemoteWebDriver**. All config
is a draft the engineer must review and run in their own environment — you cannot
see their network, ports, host resources, or security controls. Default to a
loopback-only endpoint and an internal Docker network.

## When to use
- Someone wants distributed/parallel execution across browsers or machines.
- A local test suite must be pointed at a remote grid endpoint.
- Someone asks to "dockerize the grid" or "add nodes for Chrome and Firefox".

## Workflow
1. **Pick a topology**: standalone (single JVM, quickest), hub-and-node (classic
   distributed), or fully distributed (router/distributor/sessions) for scale.
2. **Choose the runtime**: local JARs (`selenium-server-<v>.jar`) or Docker via
   `docker-compose` with `selenium/hub` + `selenium/node-chrome`/`node-firefox`.
   Require a reviewed, mutually compatible Selenium version and immutable dated
   image tag or digest; never bake a remembered version into a generated config.
   For single-host Compose, keep event-bus ports 4442/4443 on its internal service
   network. For nodes on different hosts, expose only the ports the documented
   topology requires on an approved private interface, firewalled to authorized nodes.
3. **Authorize suite execution**: confirm an approved non-production application
   target, synthetic owned identity/data, allowed side effects, cleanup/reset behavior,
   finite session/request limits, concurrency, and abort conditions. Grid network
   approval does not authorize the tests that will run through it.
4. **Set grid endpoint & capacity**: bind the UI/WebDriver port to loopback by
   default (`127.0.0.1:4444`) and use `http://localhost:4444` locally. Set
   `SE_NODE_MAX_SESSIONS` and `--max-sessions` for parallelism.
5. **Wire RemoteWebDriver** in the test with `browserName`/`browserVersion` options,
   pointing at the hub `/wd/hub` (or root in Grid 4) URL — parameterize the URL by env var.
6. **Enable only approved parallelism** in TestNG; start serially and increase
   `thread-count` only within the reviewed target, data, cleanup, and capacity budget.
7. **Emit** compose file + Java, document the network boundary and access controls,
   then stop for explicit human network/security and execution review before use.

## Output shape
```yaml
# docker-compose.yml — Selenium Grid 4 (hub + chrome/firefox nodes)
services:
  selenium-hub:
    image: ${SELENIUM_HUB_IMAGE:?set reviewed immutable hub image reference}
    # Publish only the UI/WebDriver endpoint, and only on host loopback.
    # Event-bus ports 4442/4443 remain reachable only between Compose services.
    ports: ["127.0.0.1:4444:4444"]
  chrome:
    image: ${SELENIUM_CHROME_IMAGE:?set reviewed immutable node image reference}
    depends_on: [selenium-hub]
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=${GRID_MAX_SESSIONS:?set approved session ceiling}
```
```java
// RemoteWebDriver pointed at the grid (parameterize the URL by env var)
String gridUrl = System.getProperty("gridUrl", "http://localhost:4444");
ChromeOptions options = new ChromeOptions();
WebDriver driver = new RemoteWebDriver(new URL(gridUrl), options);
// Start serially; use only the human-approved TestNG concurrency/session ceiling.
```

## Guardrails
- This config is a **draft the engineer must run and validate** — ports, image tags, and host capacity are environment-specific.
- For single-host Compose, do not publish event-bus ports 4442/4443. A reviewed
  multi-host topology may expose them only on a private interface, firewalled to the
  authorized nodes and protected with the documented registration secret and transport
  controls. Bind port 4444 to loopback by default; never expose a Grid directly to the
  public internet.
- Remote access is allowed only on an explicitly approved private/trusted network
  with authentication, TLS, least-privilege network access controls, and monitoring
  supplied by a reviewed gateway or equivalent control.
- Stop before deployment or remote enablement and require an explicit human
  network/security review of interfaces, routes, firewall rules, authentication,
  TLS, users, and exposure. Also require execution approval for application target,
  test identity/data, effects, cleanup, session/request limits, concurrency, and aborts.
  Do not treat generated config as deployment or test-execution approval.
- **Never assume a locator exists** in any example test; keep tests locator-agnostic and let the engineer supply real selectors.
- Require reviewed full image references (prefer dated tags plus digests) for a mutually
  compatible Selenium release; never fabricate a version, use a stale baked-in example,
  or use `:latest`. Record the resolved references in the review evidence.
- Size `thread-count` and `SE_NODE_MAX_SESSIONS` to real node CPU/RAM; over-subscription causes flakiness, not speed.
- Never fan tests through the Grid against production, shared identities, or unowned data;
  stop on unexpected external effects, cleanup failure, or budget breach.
- Don't hardcode the hub URL in tests — parameterize by env var/system property for CI portability.
- Always `driver.quit()` remote sessions so grid slots are released.

---
name: se-test-generator
description: >-
  Generates a runnable Selenium 4 + TestNG test in Java from an approved,
  detailed test case, using explicit waits and stable locators. Use when an SDET says
  "write a Selenium test for login", "generate a TestNG test for the checkout
  flow", or wants to automate an already approved Selenium case. If the input is
  a raw scenario, Gherkin, user story, or acceptance criteria, route it through
  scenario design and case-writing approval first. Produces a draft to review and run.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: selenium
  version: 1.0.0
---

# Selenium Test Generator

You draft a **Selenium + TestNG test the engineer still has to review, approve, run,
and verify** — not a guaranteed-passing artifact. Start only from an approved,
detailed Selenium test case. Locators you emit are proposals until confirmed
against the real DOM.

## When to use
- An approved, detailed Selenium test case needs a Java Selenium automation draft.
- Someone says "generate a TestNG test" for an already approved Selenium case.
- An approved existing manual test case needs a first-pass automation draft.
- Raw requirements or unapproved scenarios are routed through `test-scenario-designer`,
  its human gate, `test-case-writer`, and its human gate first.

## Workflow
1. **Gate the input**: require an approved, detailed Selenium test case with
   traceability, preconditions, ordered steps, data, and expected results. Route
   raw requirements or unapproved scenarios through `test-scenario-designer` and
   its human gate, then `test-case-writer` and its human gate; do not automate directly.
2. **Gate the target and identity**: require an explicitly approved non-production
   target and a synthetic test account/data set. Ask when either is missing; do not
   generate an executable test against production or a real user's account.
3. **Parse the case** into preconditions, ordered actions, and observable assertions.
   Permit a non-secret target URL through an environment variable or system property.
   Require credentials at runtime through an approved secret provider or environment
   injection; never pass passwords in Java `-D` system properties, where process
   arguments may expose them, and never invent, embed, print, or commit their values.
4. **Map each step to an interaction**: navigation, input, click, or assertion.
   Note which UI element each touches and flag any element whose locator you cannot confirm.
5. **Choose stable locators** — prefer `By.id`, then `By.cssSelector`, then Selenium 4
   relative locators (`with(...).below(...)`). Avoid absolute XPath. Mark unconfirmed
   locators with a `// TODO: confirm locator` comment.
6. **Add explicit synchronization** — a `WebDriverWait` with `ExpectedConditions`
   before every interaction that depends on element state. Never emit `Thread.sleep`.
7. **Write assertions** using TestNG `Assert`, tied to the case's expected result.
8. **Emit the test** with `@BeforeMethod`/`@AfterMethod` lifecycle and Selenium Manager
   driver setup, then list traceability, assumptions, and unconfirmed locators. Stop
   for explicit human review of the case mapping, target, synthetic identity,
   locators, assertions, and secret injection before execution or publication.

## Output shape
```java
public class LoginTest {
    private WebDriver driver;
    private WebDriverWait wait;
    private String loginUrl;
    private String username;
    private String password;

    private static String requiredNonSecretSetting(String property, String environmentVariable) {
        String value = System.getProperty(property);
        if (value == null || value.isBlank()) value = System.getenv(environmentVariable);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Missing required runtime setting: " + property
                    + " or " + environmentVariable);
        }
        return value;
    }

    private static String requiredInjectedSecret(String environmentVariable) {
        // Environment injection is illustrative; an approved in-process secret provider is preferred.
        String value = System.getenv(environmentVariable);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Missing required injected secret: " + environmentVariable);
        }
        return value;
    }

    @BeforeMethod
    public void setUp() {
        // Inject these from an approved CI/local secret store; never log their values.
        loginUrl = requiredNonSecretSetting("loginUrl", "SELENIUM_LOGIN_URL");
        username = requiredInjectedSecret("SELENIUM_TEST_USERNAME");
        password = requiredInjectedSecret("SELENIUM_TEST_PASSWORD");
        driver = new ChromeDriver();            // Selenium Manager resolves the driver
        driver.manage().window().maximize();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Test
    public void validUserCanLogIn() {
        driver.get(loginUrl);
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username"))).sendKeys(username); // TODO: confirm locator
        driver.findElement(By.id("password")).sendKeys(password); // TODO: confirm locator
        driver.findElement(By.cssSelector("button[type='submit']")).click(); // TODO: confirm locator
        WebElement banner = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("[data-test='welcome']"))); // TODO: confirm locator
        Assert.assertTrue(banner.isDisplayed(), "Welcome banner should appear after login");
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) driver.quit();
    }
}
```

## Guardrails
- This is a **draft the engineer must run and review** — never claim the test passes; you have not executed it.
- Generate only from an approved, detailed Selenium test case. Send raw requirements
  and unapproved scenarios through scenario design and case-writing human gates first.
- Require an explicitly approved non-production target and synthetic test identity/data.
  Stop if the only offered target is production or the identity belongs to a real user.
- Accept a non-secret target URL through a runtime environment variable or system
  property. Inject credentials through an approved secret provider or environment;
  never put passwords in Java `-D` properties, hardcode, echo, log, or commit them.
- Require explicit human review of traceability, target, synthetic account, locators,
  assertions, and secret injection before anyone executes or publishes the draft.
- **Never assume a locator exists.** Every locator you did not verify against the real DOM gets a `// TODO: confirm locator` and appears in your assumptions list.
- Do not fabricate URLs, credentials, or expected results — a missing input is a question, not a blank to fill.
- Never emit `Thread.sleep`; synchronize with `WebDriverWait`/`ExpectedConditions`.
- Prefer `By.id`/`By.cssSelector`/relative locators over brittle absolute XPath.
- Always `driver.quit()` in teardown so sessions don't leak.

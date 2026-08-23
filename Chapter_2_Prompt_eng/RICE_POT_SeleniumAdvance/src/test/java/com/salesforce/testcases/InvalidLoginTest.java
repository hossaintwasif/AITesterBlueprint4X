package com.salesforce.testcases;

import com.salesforce.pages.LoginPage;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import java.io.FileInputStream;
import java.io.IOException;
import java.time.Duration;
import java.util.Properties;

public class InvalidLoginTest {

    private WebDriver driver;
    private LoginPage loginPage;
    private Properties config;

    @BeforeMethod
    public void setUp() {
        try {
            config = new Properties();
            try (FileInputStream fis = new FileInputStream("src/test/resources/config.properties")) {
                config.load(fis);
            }
            WebDriverManager.chromedriver().setup();
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--start-maximized");
            driver = new ChromeDriver(options);
            driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(Long.parseLong(config.getProperty("implicit.wait.seconds"))));
            driver.get(config.getProperty("url"));
            loginPage = new LoginPage(driver, Integer.parseInt(config.getProperty("explicit.wait.seconds")));
        } catch (IOException | RuntimeException e) {
            throw new RuntimeException("Failed to initialize the WebDriver session", e);
        }
    }

    @DataProvider(name = "invalidCredentials")
    public Object[][] invalidCredentials() {
        return new Object[][]{
                {config.getProperty("invalid.username"), config.getProperty("invalid.password")}
        };
    }

    @Test(dataProvider = "invalidCredentials")
    public void verifyInvalidCredentialsShowError(String username, String password) {
        try {
            loginPage.performLogin(username, password);
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(),
                    "Error message was not displayed for invalid credentials");
            Assert.assertTrue(loginPage.getErrorMessage().contains("check your username and password"),
                    "Unexpected error message text: " + loginPage.getErrorMessage());
        } catch (AssertionError | RuntimeException e) {
            throw e;
        }
    }

    @Test
    public void verifyEmptyFieldsShowError() {
        try {
            loginPage.performLogin("", "");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(),
                    "Error message was not displayed for empty credentials");
        } catch (AssertionError | RuntimeException e) {
            throw e;
        }
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}

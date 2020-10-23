import org.openqa.selenium.WebDriver
import org.openqa.selenium.firefox.FirefoxDriver

WebDriver driver = new FirefoxDriver()
driver.manage().timeouts().implicitlyWait(30,TimeUnit.SECONDS)
driver.get("http://www.google.com")

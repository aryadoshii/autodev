// tests/user-flow.spec.js
const { test, expect } = require('@playwright/test');
const fs = require('fs');

// Page Object Models
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async navigateToLogin() {
    await this.page.goto('/login');
    await expect(this.page).toHaveURL(/\/login/);
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

class RegisterPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="register-email-input"]');
    this.passwordInput = page.locator('[data-testid="register-password-input"]');
    this.confirmPasswordInput = page.locator('[data-testid="confirm-password-input"]');
    this.registerButton = page.locator('[data-testid="register-button"]');
    this.successMessage = page.locator('[data-testid="success-message"]');
  }

  async navigateToRegister() {
    await this.page.goto('/register');
    await expect(this.page).toHaveURL(/\/register/);
  }

  async register(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.confirmPasswordInput.fill(password);
    await this.registerButton.click();
  }
}

class DashboardPage {
  constructor(page) {
    this.page = page;
    this.dashboardTitle = page.locator('[data-testid="dashboard-title"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
    this.addItemButton = page.locator('[data-testid="add-item-button"]');
    this.itemList = page.locator('[data-testid="item-list"]');
    this.itemRows = page.locator('[data-testid="item-row"]');
  }

  async isDashboardVisible() {
    await expect(this.dashboardTitle).toBeVisible();
  }

  async logout() {
    await this.logoutButton.click();
  }

  async addItem(name) {
    await this.addItemButton.click();
    const modal = this.page.locator('[data-testid="item-modal"]');
    await expect(modal).toBeVisible();
    
    const nameInput = this.page.locator('[data-testid="item-name-input"]');
    const saveButton = this.page.locator('[data-testid="save-item-button"]');
    
    await nameInput.fill(name);
    await saveButton.click();
  }

  async getItemRowByName(name) {
    return this.page.locator(`[data-testid="item-row"] >> text=${name}`);
  }

  async editItem(oldName, newName) {
    const row = await this.getItemRowByName(oldName);
    await row.locator('[data-testid="edit-item-button"]').click();
    
    const modal = this.page.locator('[data-testid="item-modal"]');
    await expect(modal).toBeVisible();
    
    const nameInput = this.page.locator('[data-testid="item-name-input"]');
    const saveButton = this.page.locator('[data-testid="save-item-button"]');
    
    await nameInput.fill(newName);
    await saveButton.click();
  }

  async deleteItem(name) {
    const row = await this.getItemRowByName(name);
    await row.locator('[data-testid="delete-item-button"]').click();
    
    // Confirm deletion
    const confirmButton = this.page.locator('[data-testid="confirm-delete-button"]');
    await expect(confirmButton).toBeVisible();
    await confirmButton.click();
  }
}

class ProtectedPage {
  constructor(page) {
    this.page = page;
    this.protectedContent = page.locator('[data-testid="protected-content"]');
  }

  async navigate() {
    await this.page.goto('/protected');
  }

  async isProtectedContentVisible() {
    await expect(this.protectedContent).toBeVisible();
  }
}

// Test suite
test.describe('User Flow Tests', () => {
  let loginPage;
  let registerPage;
  let dashboardPage;
  let protectedPage;
  const testUser = {
    email: `testuser${Date.now()}@example.com`,
    password: 'TestPass123!'
  };

  test.beforeEach(async ({ page }) => {
    // Initialize page objects
    loginPage = new LoginPage(page);
    registerPage = new RegisterPage(page);
    dashboardPage = new DashboardPage(page);
    protectedPage = new ProtectedPage(page);
    
    // Set viewport for better screenshots
    await page.setViewportSize({ width: 1280, height: 720 });
  });

  test.afterEach(async ({ page }, testInfo) => {
    // Take screenshot on failure
    if (testInfo.status !== testInfo.expectedStatus) {
      const screenshotPath = `screenshots/${testInfo.title}.png`;
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`Screenshot saved to ${screenshotPath}`);
    }
  });

  test('1. User Registration Flow', async ({ page }) => {
    // Navigate to register page
    await registerPage.navigateToRegister();
    
    // Fill form with valid data
    await registerPage.register(testUser.email, testUser.password);
    
    // Verify success message
    await expect(registerPage.successMessage).toBeVisible();
    await expect(registerPage.successMessage).toContainText('Registration successful');
    
    // Verify redirect to login
    await expect(page).toHaveURL(/\/login/);
  });

  test('2. User Login Flow', async ({ page }) => {
    // Navigate to login page
    await loginPage.navigateToLogin();
    
    // Enter credentials
    await loginPage.login(testUser.email, testUser.password);
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/);
    
    // Verify dashboard is visible
    await dashboardPage.isDashboardVisible();
    
    // Verify token is stored (by checking that we can access protected content)
    await expect(loginPage.page.locator('[data-testid="user-email"]')).toHaveText(testUser.email);
  });

  test('3. CRUD Operations Flow', async ({ page }) => {
    // Login as user
    await loginPage.navigateToLogin();
    await loginPage.login(testUser.email, testUser.password);
    await dashboardPage.isDashboardVisible();
    
    // Create new item
    const itemName = `Test Item ${Date.now()}`;
    await dashboardPage.addItem(itemName);
    
    // Verify item appears in list
    const itemRow = await dashboardPage.getItemRowByName(itemName);
    await expect(itemRow).toBeVisible();
    
    // Edit item
    const editedItemName = `${itemName} - Edited`;
    await dashboardPage.editItem(itemName, editedItemName);
    
    // Verify item is updated
    const editedItemRow = await dashboardPage.getItemRowByName(editedItemName);
    await expect(editedItemRow).toBeVisible();
    
    // Delete item
    await dashboardPage.deleteItem(editedItemName);
    
    // Verify item is deleted
    const deletedItemRow = await dashboardPage.getItemRowByName(editedItemName);
    await expect(deletedItemRow).not.toBeVisible();
  });

  test('4. Authentication Flow', async ({ page }) => {
    // Access protected page without login
    await protectedPage.navigate();
    
    // Verify redirect to login
    await expect(page).toHaveURL(/\/login/);
    
    // Login and access protected page
    await loginPage.navigateToLogin();
    await loginPage.login(testUser.email, testUser.password);
    await protectedPage.navigate();
    
    // Verify access to protected content
    await protectedPage.isProtectedContentVisible();
    
    // Logout and verify redirect
    await dashboardPage.logout();
    await expect(page).toHaveURL(/\/login/);
    
    // Try to access protected page again after logout
    await protectedPage.navigate();
    await expect(page).toHaveURL(/\/login/);
  });
});
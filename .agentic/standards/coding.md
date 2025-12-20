# 💻 Coding Standards

## Naming Conventions
| Context | Convention | Example |
|---------|------------|---------|
| Python vars | snake_case | user_name |
| Python classes | PascalCase | UserService |
| TypeScript | camelCase | userName |
| JSON keys | camelCase | firstName |
| API URLs | kebab-case | /user-profiles/ |

## Patterns
- Services: Business logic (write operations)
- Selectors: Read operations
- APIs: Thin controllers, delegate to services

---
applyTo: "**/*.bicep"
---

# Bicep Development Standards

## 1. Project Structure and Organization

- All Bicep code is located in the `infrastructure/` folder
- Use single-purpose, reusable modules
- Default `targetScope = 'subscription'` for main templates, `targetScope = 'resourceGroup'` for modules
- **ALL Azure resources must be defined in Bicep files** - including resource groups and any other infrastructure components
- **ALL configuration parameters must be in .bicepparam files** - deployment scripts should contain no hardcoded values
- Deployment scripts should only orchestrate the deployment, not define infrastructure or configuration

## 2. Naming Conventions

Use prefixes for all Bicep elements to ensure clarity and consistency:

- **Parameters**: `paramName` (camelCase)
- **Variables**: `varName` (camelCase)
- **Outputs**: `outputName` (camelCase)
- **Modules**: `modName` (camelCase)
- **Resources**: `resName` (camelCase)

### Resource Naming Example

```bicep
// CORRECT
param paramStorageAccountPrefix string
var varStorageAccountName = '${paramStorageAccountPrefix}${uniqueString(resourceGroup().id)}'

// INCORRECT
var storageAccountName = 'mystorageaccount123' // Hardcoded names
```

## 3. Parameter Standards

### Parameter Definition Best Practices

- Include `@description` for each parameter
- Use `@allowed`, `@minLength`/`@maxLength` and `@minValue`/`@maxValue` where applicable
- Provide sensible defaults and conditional values based on environment
- **NEVER provide default values for secure parameters** (except empty strings or newGuid())

### Parameter References

- When referencing parameters between modules, ensure they're actually defined in the target module
- Check parameter definitions in module files before passing values

## 4. Resource Standards

### Resource Declarations

- Avoid unnecessary string interpolation like `'${singleVariable}'` (use the variable directly)
- Remove all unused variables and resources
- Use `environment().suffixes` for service hostnames (like database.windows.net) to ensure cloud portability

### Module References

- Use IDE features (if available) to validate parameter names before deployment
- When updating module interfaces, ensure all calling code is updated accordingly
- For complex integrations like Key Vault access policies, prefer separate modules with specific responsibilities

## 5. Validation and Quality Assurance

### Bicep Validation Process

- Run `az bicep build --file main.bicep` to catch all errors and warnings
- Make sure that all .json files generated from Bicep are not checked into source control and are deleted right after verification
- Verify all module parameter references match the actual module parameters
- Remove unnecessary dependsOn entries
- Check that Key Vault references and permission assignments are properly configured
- Avoid using `listCredentials()` directly in module parameters

## 6. Deployment Guidelines

- You are not allowed to actually deploy Bicep files yourself. This will always be done by the user
- The `az bicep` commands automatically transpile Bicep to JSON, so explicit JSON conversion is not required
# Gateway API Migration Guide

## Overview

This Helm chart has been updated to support the modern Gateway API alongside the traditional Ingress API. Gateway API provides enhanced features, better security, and more flexibility for enterprise deployments.

## Migration Status

- **Current Default**: Ingress API (for backward compatibility)
- **Recommended for New Deployments**: Gateway API
- **Deprecation Notice**: Ingress API will be deprecated in a future version

## Prerequisites for Gateway API

1. **Gateway API CRDs**: Install Gateway API CRDs in your cluster
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
   ```

2. **Gateway Controller**: Install a Gateway API controller (e.g., nginx-gateway-fabric, istio, envoy-gateway)
   ```bash
   # Example for nginx-gateway-fabric
   kubectl apply -f https://github.com/nginxinc/nginx-gateway-fabric/releases/download/v1.0.0/nginx-gateway-fabric.yaml
   ```

## Migration Steps

### Step 1: Prepare Your Environment
Ensure your cluster has Gateway API support:
```bash
# Check if Gateway API CRDs are installed
kubectl api-resources | grep gateway.networking.k8s.io

# Expected output should include:
# gatewayclasses      gc           gateway.networking.k8s.io/v1    false        GatewayClass
# gateways           gtw          gateway.networking.k8s.io/v1    true         Gateway
# httproutes         hr           gateway.networking.k8s.io/v1    true         HTTPRoute
```

### Step 2: Test Gateway API Configuration
Create a test values file to validate Gateway API works in your environment:

```yaml
# values-gateway-migration.yaml
ingress:
  enabled: false

gateway:
  enabled: true
  gatewayClassName: "nginx"  # or your preferred gateway class
  hostname: "your-domain.com"
  tls:
    enabled: true
    secretName: "your-tls-secret"
```

Deploy with test values:
```bash
helm upgrade --install my-release . -f values-gateway-migration.yaml --dry-run
```

### Step 3: Update Your Production Values
Update your production values.yaml:

```yaml
# Disable Ingress API (after testing)
ingress:
  enabled: false

# Enable Gateway API
gateway:
  enabled: true
  gatewayClassName: "your-gateway-class"
  hostname: "your-production-domain.com"
  
  # Enterprise security features
  tls:
    enabled: true
    secretName: "your-production-tls-secret"
  
  # Optional: Custom annotations for your gateway controller
  annotations:
    # Example for rate limiting
    nginx.org/rate-limit: "100r/s"
    # Example for timeout configuration
    nginx.org/timeout-upstream: "30s"
```

### Step 4: Deploy with Gateway API
```bash
helm upgrade --install my-release . -f values.yaml
```

## Feature Comparison

| Feature | Ingress API | Gateway API | Notes |
|---------|-------------|-------------|-------|
| Basic HTTP routing | ✅ | ✅ | Both support path-based routing |
| TLS termination | ✅ | ✅ | Gateway API has more flexible TLS config |
| Header manipulation | ⚠️ | ✅ | Limited in Ingress, comprehensive in Gateway API |
| Traffic splitting | ❌ | ✅ | Gateway API supports weighted routing |
| Cross-namespace routing | ❌ | ✅ | Gateway API supports cross-namespace routes |
| Security headers | ⚠️ | ✅ | Annotation-based vs native support |
| NetworkPolicy integration | ❌ | ✅ | Automatic NetworkPolicy with Gateway API |

## Enterprise Security Features

When using Gateway API, the following security features are automatically enabled:

### Security Headers
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- Content Security Policy

### Network Security
- Automatic NetworkPolicy creation
- Restricted ingress/egress rules
- Namespace isolation

### CORS Configuration
- Proper CORS headers for API endpoints
- Configurable allowed origins, methods, and headers

## Troubleshooting

### Common Issues

1. **Gateway API CRDs not installed**
   ```
   Error: no matches for kind "Gateway" in version "gateway.networking.k8s.io/v1"
   ```
   Solution: Install Gateway API CRDs as described in prerequisites.

2. **No GatewayClass available**
   ```
   Error: Gateway references a GatewayClass that does not exist
   ```
   Solution: Install a Gateway API controller or check the `gatewayClassName` in your values.

3. **TLS certificate issues**
   ```
   Error: certificateRef secret not found
   ```
   Solution: Ensure your TLS secret exists in the same namespace as the Gateway.

### Validation
The chart includes validation to prevent common configuration errors:
- Cannot enable both Ingress and Gateway API simultaneously
- Must enable at least one networking option
- Validates required fields for each networking option

## Rollback Procedure

If you need to rollback to Ingress API:

1. Update your values.yaml:
   ```yaml
   ingress:
     enabled: true
   gateway:
     enabled: false
   ```

2. Upgrade the release:
   ```bash
   helm upgrade my-release . -f values.yaml
   ```

## Support

For issues related to:
- Gateway API functionality: Check the [Gateway API documentation](https://gateway-api.sigs.k8s.io/)
- Gateway controllers: Refer to your specific controller's documentation
- Chart configuration: Review the values.yaml file and this migration guide
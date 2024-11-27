# API 文档

## 认证方法

### 1. API 密钥认证
最基本的认证方式，通过在请求头中添加 API 密钥进行身份验证：
```http
Authorization: Bearer your-api-key-here
```

### 2. OAuth 2.0
更安全的认证方式，支持多种授权流程：
- 授权码流程
- 客户端凭证流程
- 密码凭证流程
- 隐式授权流程

### 3. JWT (JSON Web Tokens)
基于令牌的认证机制，适用于分布式系统：
```javascript
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

## API 端点

### 用户管理
- GET /users - 获取用户列表
- POST /users - 创建新用户
- PUT /users/{id} - 更新用户信息
- DELETE /users/{id} - 删除用户

### 数据操作
- GET /data - 获取数据
- POST /data - 创建数据
- PUT /data/{id} - 更新数据
- DELETE /data/{id} - 删除数据 
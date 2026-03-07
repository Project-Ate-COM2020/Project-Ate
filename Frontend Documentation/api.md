# API Module Documentation

This module provides 4 functions for communicating with the backend: 2 async functions for event-driven requests (forms, buttons) and 2 React hooks for automatic data fetching (badges, ).

## Async Functions

Use these in event handlers like form submissions or button clicks.

### `getData(endpoint, queryParams = {}, authenticate = true)`

Fetch data from the backend using GET.

**Parameters:**

- `endpoint` (string): API path (e.g., `"marketplace/bundle"`)
- `queryParams` (object): URL query parameters (optional, e.g., `{ id: 123 }`)
- `authenticate` (boolean): Include authorization header (needed unless user is not logged in) (default: `true`)

**Returns:** Promise resolving to JSON response data

**Example:**

```javascript
import { getData } from '../api/api';

const data = await getData('marketplace/bundle', { id: 5 }, true);
console.log(data);
```

---

### `postData(endpoint, postData, authenticate = true)`

Send data to the backend using POST.

**Parameters:**

- `endpoint` (string): API path (e.g., `"marketplace/seller"`)
- `postData` (object): Data to send in request body
- `authenticate` (boolean): Include authorization header (needed unless user is not logged in) (default: `true`)

**Returns:** Promise resolving to JSON response data

**Example:**

```javascript
import { postData } from '../api/api';

const response = await postData('marketplace/seller', {
  name: 'My Shop',
  email: 'shop@example.com'
}, true);
```

---

## React Hooks

Use these in components to automatically fetch data for a page - does not require page refresh to update

### `useGetData(endpoint, queryParams = {}, authenticate = true)`

Hook for automatic GET requests.

**Parameters:** Same as `getData()`

**Returns:** Object with `{ data, loading }`

- `data`: Response data or `null` while loading
- `loading`: Boolean indicating if request is in progress

**Example:**

```javascript
import { useGetData } from '../api/api';

function MyComponent() {
  const { data, loading } = useGetData('marketplace/bundles', {}, true);

  if (loading) return <div>Loading...</div>;
  return <div>{JSON.stringify(data)}</div>;
}
```

---

### `usePostData(endpoint, postData, authenticate = true)`

Hook for automatic POST requests

**Parameters:** Same as `postData()`

**Returns:** Object with `{ data, loading }`

**Example:**

```javascript
import { usePostData } from '../api/api';

function MyComponent() {
  const payload = { name: 'test' };
  const { data, loading } = usePostData('marketplace/seller', payload, true);

  if (loading) return <div>Loading...</div>;
  return <div>Result: {JSON.stringify(data)}</div>;
}
```

---

## Token Refresh

All functions automatically handle expired tokens:

- If a request returns `401` (Unauthorized), the module calls `refreshTokens()` internally
- Retries the request once with the new token
- If refresh fails, returns the original `401` response

---

## Current Problems / Future Development

There are a number of notes for the future of this library:

- There is currently no graceful error handling - if a backend endpoint cannot be reached or returns unexpected data then the program immediately crashes - will fix when I get time

- Currently relies on a new cookie user_type being introduced, either containing "buyer" or "seller" - this would have to be worked so that this is only introduced after cookies have been accepted e.g: during login

---

### Warning

DO NOT TRY TO IMPLEMENT INDIVIDUAL FIXES FOR AUTH - IF THIS LIBRARY CANNOT HANDLE A FUNCTION YOU NEED OR YOU HAVE FOUND A BUG, PLEASE LET ME KNOW

---

#### Authored by Jamie Jamie

##### 06/03/2026

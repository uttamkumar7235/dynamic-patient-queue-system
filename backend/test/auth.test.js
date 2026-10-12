const test = require('node:test');
const assert = require('node:assert/strict');
const bcrypt = require('bcryptjs');

const { registerUser, loginUser } = require('../src/controllers/authController');
const { authenticate, authorize } = require('../src/middleware/auth');

test('registerUser creates a PATIENT account and hashes the password', async () => {
  const users = [];
  const UserModel = {
    async findOne({ email }) {
      return users.find((user) => user.email === email) || null;
    },
    async create(data) {
      const user = {
        _id: 'user-1',
        ...data
      };
      users.push(user);
      return user;
    }
  };

  const result = await registerUser({
    UserModel,
    body: {
      name: 'Alice Smith',
      email: 'alice@example.com',
      password: 'Secret1234'
    }
  });

  assert.equal(result.user.role, 'PATIENT');
  assert.equal(result.user.email, 'alice@example.com');
  assert.equal(users[0].role, 'PATIENT');
  assert.match(users[0].passwordHash, /^\$2[aby]?\$/);
  assert.ok(result.token.length > 20);
});

test('registerUser rejects public registration for non-PATIENT roles', async () => {
  const UserModel = {
    async findOne() {
      return null;
    },
    async create() {
      return null;
    }
  };

  await assert.rejects(
    () =>
      registerUser({
        UserModel,
        body: {
          name: 'Dr. Patel',
          email: 'doctor@example.com',
          password: 'Secret1234',
          role: 'DOCTOR'
        }
      }),
    {
      message: 'Public registration is restricted to PATIENT accounts.'
    }
  );
});

test('loginUser verifies the password and returns a JWT', async () => {
  const passwordHash = await bcrypt.hash('Secret1234', 10);
  const UserModel = {
    async findOne({ email }) {
      if (email === 'bob@example.com') {
        return {
          _id: 'user-2',
          name: 'Bob Jones',
          email: 'bob@example.com',
          role: 'DOCTOR',
          passwordHash
        };
      }
      return null;
    }
  };

  const result = await loginUser({
    UserModel,
    body: {
      email: 'bob@example.com',
      password: 'Secret1234'
    }
  });

  assert.equal(result.user.role, 'DOCTOR');
  assert.equal(result.user.email, 'bob@example.com');
  assert.ok(result.token.length > 20);
});

test('authenticate rejects missing or invalid bearer tokens', async () => {
  const req = { headers: {} };
  const res = {
    statusCode: 200,
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(payload) {
      this.payload = payload;
      return this;
    }
  };

  let nextCalled = false;
  await authenticate(req, res, () => {
    nextCalled = true;
  });

  assert.equal(res.statusCode, 401);
  assert.equal(nextCalled, false);
});

test('authorize allows the correct role and blocks others', async () => {
  const allowed = { headers: {}, user: { role: 'DOCTOR' } };
  const blocked = { headers: {}, user: { role: 'PATIENT' } };

  let nextCalled = false;
  const next = () => {
    nextCalled = true;
  };

  const res = {
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(payload) {
      this.payload = payload;
      return this;
    }
  };

  authorize('DOCTOR', 'STAFF')(allowed, res, next);
  assert.equal(nextCalled, true);

  nextCalled = false;
  authorize('DOCTOR', 'STAFF')(blocked, res, next);
  assert.equal(nextCalled, false);
  assert.equal(res.statusCode, 403);
});

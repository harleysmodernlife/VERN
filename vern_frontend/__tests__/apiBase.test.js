/**
 * Tests for getApiBase() precedence:
 * 1) window.__VERN_API_BASE__
 * 2) process.env.NEXT_PUBLIC_API_BASE
 * 3) same-origin (empty string)
 */
import { getApiBase, joinApi } from "../lib/apiBase";

describe("apiBase", () => {
  const OLD_ENV = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...OLD_ENV };
    delete process.env.NEXT_PUBLIC_API_BASE;
    // Ensure no global.window leaks between tests
    // Note: deleting global.window simulates non-browser env
    // and allows us to explicitly set it when needed.
    // @ts-ignore
    delete global.window;
  });

  afterEach(() => {
    process.env = OLD_ENV;
    // @ts-ignore
    delete global.window;
  });

  test("prefers window.__VERN_API_BASE__", () => {
    // @ts-ignore
    global.window = { __VERN_API_BASE__: "http://example.com/api" };
    expect(getApiBase()).toBe("http://example.com/api");
  });

  test("uses NEXT_PUBLIC_API_BASE when window not set", () => {
    process.env.NEXT_PUBLIC_API_BASE = "http://env.example/api";
    expect(getApiBase()).toBe("http://env.example/api");
  });

  test("defaults to empty base", () => {
    expect(getApiBase()).toBe("");
  });

  test("joinApi concatenates with leading slash", () => {
    // @ts-ignore
    global.window = { __VERN_API_BASE__: "http://example.com/api" };
    expect(joinApi("/agents/status")).toBe("http://example.com/api/agents/status");
  });

  test("joinApi with bare path", () => {
    process.env.NEXT_PUBLIC_API_BASE = "http://env.example/api";
    expect(joinApi("agents/status")).toBe("http://env.example/api/agents/status");
  });

  test("joinApi with empty base stays same-origin", () => {
    expect(joinApi("/agents/status")).toBe("/agents/status");
  });
});
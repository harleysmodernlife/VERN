export function getApiBase() {
  if (typeof window !== "undefined" && window.__VERN_API_BASE__) return window.__VERN_API_BASE__;
  if (process.env.NEXT_PUBLIC_API_BASE) return process.env.NEXT_PUBLIC_API_BASE;
  return "";
}
export function joinApi(path) {
  const base = getApiBase();
  if (!path) return base;
  if (base && path.startsWith("/")) return base + path;
  return base ? base + "/" + path : path;
}
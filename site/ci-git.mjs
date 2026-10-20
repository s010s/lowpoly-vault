/** Exact-commit evidence must read original Git objects, never local replace refs
 * or graft files that can rewrite ancestry without changing a commit hash.
 * Supply this environment to every Git invocation and to publication child
 * processes that may themselves read Git. Do not mutate process-global state.
 */
export function immutableGitEnv(environment = process.env) {
  return {...environment, GIT_NO_REPLACE_OBJECTS: '1', GIT_GRAFT_FILE: '/dev/null'};
}

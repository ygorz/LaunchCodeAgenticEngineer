# PRD: Docker Setup Review

This workflow reviews a repository’s Docker setup by running the documented build command, reporting the outcome, and recommending whether the repo is ready to proceed.

Trigger: A developer manually runs Claude Code from the module_1 root inside the agentic_engineer_1 container and prompts it to review the repository's Docker setup. Preconditions: the container is running with the repo mounted, and Claude Code is logged in.

Decision Events:
- If the Docker build succeeds, the agent summarizes any warnings and recommends proceeding.
- If the Docker build fails, the agent reports the error output and recommends against proceeding. It does not attempt a fix.
- If no documented build command can be found, the agent reports that and stops without guessing one.

Actions:
1. Read the repository's documentation to identify the documented Docker build command. If none is found, report that and stop.
2. Run the documented Docker build command inside the sandbox.
3. Capture the full build output and exit code.
4. Determine whether the build succeeded or failed, based on the exit code and output.
5. Summarize every warning and error in the output.
6. Give a final recommendation, either ready to proceed or not ready, with a brief rationale tied to the build result.

Acceptance Criteria:
- The agent identifies and quotes the documented Docker build command it used, or states that none was found and stops without running a build.
- The agent correctly states whether the Docker build succeeded or failed, and reports the exit code.
- The summary includes all warnings and errors present in the build output; it does not omit any.
- The recommendation (ready to proceed or not ready) is consistent with the build result.
- If the build failed, the agent did not modify any files to attempt a fix.
- The agent did not push, publish, or deploy anything.
# 1. Quality Rubric

## 1.1 Dimensions

### 1.1.1 Build Result Accuracy

Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result, success or failure, to match the actual exit status of the build command.

### 1.1.2 Warning and Error Coverage

Measures whether the agent's summary includes every warning and error present in the build output. A high score requires no omissions and no invented issues.

### 1.1.3 Recommendation Consistency

Measures whether the final recommendation, ready to proceed or not ready, matches the build result. A high score requires a brief rationale tied directly to that result.

## 1.2 Alternatives Considered

- Scoring "No fix attempted" and "No push, publish, or deploy" as dimensions. Ruled out because they are yes-or-no safety rules with no meaningful partial credit, so they stay as gates outside the score.
- A separate dimension for finding the documented build command. Ruled out because that case is already handled as a decision event and acceptance criterion (report and stop if none is found), so a separate score would double-count it.
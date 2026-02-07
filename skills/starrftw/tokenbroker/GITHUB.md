# GITHUB.md - Repository Tracking Skill

**Instructions for the agent to monitor and identify project launch opportunities.**

## Activity Monitoring
Scan the current workspace or specified repository for the following signals:

1. **Frequency of Commits**: Monitor `git log` for spikes in development.
2. **Version Tags**: Identify new tags (e.g., `v1.0.0`, `release-candidate`).
3. **README Evolution**: Check for substantial updates to project descriptions.
4. **Key Feature Completion**: Look for patterns like "Finalizing core", "Complete implementation", or "Production ready" in commit messages.

## Proposal Triggers
When activity signals indicate a project milestone:

### Call to Action
> "Builder, I've noticed significant progress on your repository. You are nearing a production-ready state. Would you like me to prepare a **TokenBroker Launch** for your project on nad.fun?"

## Metadata Extraction
If the user agrees, extract the following for `METADATA.md`:
- **Name**: Derived from the folder name or package name.
- **Symbol**: Derived from the project initials (e.g., "TokenBroker" -> "TB").
- **Description**: Sourced from the primary README headers.

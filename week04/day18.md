# Day18 - Git Workflow Practice

## Goal

Practice the standard local development workflow:

1. Fetch the latest remote state
2. Edit files in VS Code
3. Review changes with Diff
4. Commit changes locally
5. Push changes to GitHub
6. Verify the published result

---

## What I Practiced

I practiced the Git workflow with both a new file and an existing file.

### New File

A newly created file appeared as:

`U = Untracked`

This means Git recognizes the file, but it has not yet been committed.

### Existing File

After modifying an existing file, it appeared as:

`M = Modified`

This means Git detected changes to a file that is already tracked.

---

## Key Git Concepts

- **Fetch** checks whether GitHub has newer changes.
- **Pull** brings remote changes into the local repository.
- **Diff** shows exactly what changed before committing.
- **Commit** records a local snapshot of changes.
- **Push** sends local commits to GitHub.

---

## Development Workflow

VS Code → Review Diff → Commit → Push → GitHub

GitHub Desktop provides a visual interface for Git operations, while GitHub Web is used to verify the published repository.

---

## Plain-English Summary

Git provides a structured way to track and share changes.

Before publishing a change, I can review exactly what changed, record that change locally with a commit, and then push it to GitHub.

This creates a clear and traceable development history.

---

## What Humans Should Check

Before committing or pushing:

- Confirm that only intended files were changed.
- Review the Diff for unexpected modifications.
- Use a clear commit message.
- Confirm that files are in the correct directory.
- Verify the final result on GitHub after pushing.

---

## Platform Builder View

Git is more than a code storage mechanism.

A reliable Git workflow provides traceability, controlled change management, collaboration, and a clear history of how a platform evolves.

Understanding this workflow is foundational for working effectively with engineering teams and AI-assisted development tools.
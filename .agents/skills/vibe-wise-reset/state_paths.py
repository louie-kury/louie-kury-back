"""Project boundary lookup from VibeWise; no session hook is registered."""
from pathlib import Path


def git_root(cwd):
    """Find the nearest repository or worktree root (a .git directory or file)."""
    for directory in (cwd, *cwd.parents):
        if (directory / ".git").exists():
            return directory
    return None


def state_directory(cwd):
    """Find the nearest notes directory without crossing a Git project boundary."""
    root = git_root(cwd)
    # Within Git, a source subdirectory should still find the project's notes.
    # Without Git there's no project boundary, so only the starting folder counts:
    # searching upward could adopt notes from an unrelated parent folder.
    candidates = [cwd] if root is None else [cwd, *cwd.parents][
        : len(cwd.relative_to(root).parts) + 1
    ]
    for directory in candidates:
        # Prefer the new name at the nearest location; keep legacy notes in place.
        for name in (".vibe-wise", ".sensible-vibes"):
            state = directory / name
            if state.exists() or state.is_symlink():
                # Stop even if this candidate is invalid. Falling back to a parent
                # could silently load a different project's learner profile.
                return state if state.is_dir() and not state.is_symlink() else None
    return None

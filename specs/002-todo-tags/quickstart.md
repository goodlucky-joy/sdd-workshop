# Quick Start: Todo Tags Feature

**Feature**: `002-todo-tags`
**Time to Complete**: 5 minutes

## Overview

Add categorization to your todos with tags! This feature lets you attach up to 5 tags to each todo and filter your list by tags.

## Getting Started

### 1. Add Todos with Tags

```bash
# Add a todo with a single tag
todo add "Complete project proposal" --tag work

# Add a todo with multiple tags
todo add "Prepare presentation slides" --tag work --tag urgent --tag meeting

# Add a todo with all options
todo add "Fix critical bug" --due 2026-05-10 --priority HIGH --tag bug --tag critical
```

### 2. View Your Tagged Todos

```bash
# List all todos (tagged ones show with brackets)
todo list

# Example output:
# 1. [work] Complete project proposal
# 2. [work, urgent, meeting] Prepare presentation slides
# 3. [bug, critical] Fix critical bug (HIGH) - Due: 2026-05-10
```

### 3. Filter by Tags

```bash
# Show only todos with 'work' tag
todo list --tag work

# Combine with other filters
todo list --tag urgent --filter pending --priority HIGH
```

## Tag Rules

- **Maximum 5 tags** per todo
- **Each tag ≤ 20 characters**
- **No duplicate tags** (case-insensitive)
- **Unicode supported** (Korean, emojis, etc.)
- **Case-insensitive filtering**

## Examples

### Basic Usage
```bash
# Create categorized todos
todo add "Buy groceries" --tag personal
todo add "Review code" --tag work --tag review
todo add "Call mom" --tag personal --tag family

# View all
todo list
# 1. [personal] Buy groceries
# 2. [work, review] Review code
# 3. [personal, family] Call mom

# Filter by category
todo list --tag personal
# 1. [personal] Buy groceries
# 3. [personal, family] Call mom

todo list --tag work
# 2. [work, review] Review code
```

### Advanced Filtering
```bash
# High priority work items
todo list --tag work --priority HIGH

# Urgent items that aren't done yet
todo list --tag urgent --filter pending

# Family-related tasks with any priority
todo list --tag family
```

## Common Patterns

### Work-Life Balance
```bash
# Work tasks
todo add "Team meeting" --tag work --tag meeting
todo add "Code review" --tag work --tag review

# Personal tasks
todo add "Exercise" --tag personal --tag health
todo add "Read book" --tag personal --tag leisure

# Quick filtering
todo list --tag work      # Work only
todo list --tag personal  # Personal only
```

### Priority Management
```bash
# Critical items
todo add "Fix server outage" --priority HIGH --tag bug --tag critical

# Important but not urgent
todo add "Update documentation" --priority MEDIUM --tag work --tag docs

# Nice to have
todo add "Clean desk" --priority LOW --tag personal --tag chore
```

## Tips

- **Use consistent tag names**: "work" vs "Work" are treated as the same
- **Keep tags short**: Use abbreviations like "mtg" for "meeting"
- **Combine filters**: `--tag work --priority HIGH` finds important work items
- **Review regularly**: `todo list --tag work` to see your work tasks

## Troubleshooting

### Common Errors
```
Error: Too many tags (max 5)
# Solution: Remove some tags, keep only the most important 5

Error: Tag too long (max 20 chars): 'very_long_tag_name_here'
# Solution: Shorten the tag or use an abbreviation

Error: Duplicate tag: 'work'
# Solution: Remove the duplicate, tags are case-insensitive
```

### Getting Help
```bash
# See all available options
todo add --help
todo list --help
```

## What's Next?

- **Mark complete**: `todo done <id>`
- **Delete**: `todo delete <id>`
- **More filtering**: Combine tags with priority and status filters

Happy organizing! 🎯

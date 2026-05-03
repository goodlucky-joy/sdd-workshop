# CLI Contract: Todo Tags Feature

**Feature**: `002-todo-tags`
**Date**: 2026-05-03
**Contract Type**: Command Line Interface

## Overview

This contract defines the CLI interface for the Todo Tags feature. The CLI maintains backward compatibility while adding tag functionality to the `add` and `list` commands.

## Command Specifications

### 1. Add Command

**Command**: `todo add <title> [options]`

**Purpose**: Create a new Todo item with optional tags

#### Syntax
```
todo add <title> [--due <date>] [--priority <level>] [--tag <tag>]...
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | String | Yes | Todo description (max 255 chars) |
| `--due` | Date | No | Due date (YYYY-MM-DD format) |
| `--priority` | Enum | No | Priority level: HIGH, MEDIUM, LOW |
| `--tag` | String | No | Tag to attach (repeatable, max 5 tags) |

#### Tag Validation Rules
- **Maximum tags**: 5 per Todo
- **Tag length**: 1-20 characters
- **Uniqueness**: No duplicate tags (case-insensitive)
- **Content**: Non-empty after whitespace trimming
- **Unicode**: Full Unicode support

#### Examples
```bash
# Basic todo (no tags)
todo add "Buy groceries"

# Todo with single tag
todo add "Complete project proposal" --tag work

# Todo with multiple tags
todo add "Prepare presentation" --tag work --tag urgent --tag meeting

# Todo with all options
todo add "Fix critical bug" --due 2026-05-10 --priority HIGH --tag bug --tag urgent
```

#### Error Handling
| Error Condition | Exit Code | Error Message |
|----------------|-----------|---------------|
| Missing title | 2 | Error: Missing argument 'TITLE' |
| Invalid date format | 2 | Error: Invalid value for '--due' |
| Invalid priority | 2 | Error: Invalid choice |
| Too many tags | 1 | Error: Too many tags (max 5) |
| Tag too long | 1 | Error: Tag too long (max 20 chars): 'very_long_tag_name' |
| Duplicate tags | 1 | Error: Duplicate tag: 'work' |
| Database error | 1 | Error: Failed to save todo |

#### Success Response
```
Todo added successfully (ID: 42)
```

### 2. List Command

**Command**: `todo list [options]`

**Purpose**: List Todo items with optional filtering

#### Syntax
```
todo list [--filter <status>] [--priority <level>] [--tag <tag>]
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--filter` | Enum | No | Status filter: all, done, pending |
| `--priority` | Enum | No | Priority filter: HIGH, MEDIUM, LOW |
| `--tag` | String | No | Tag filter (case-insensitive) |

#### Filtering Logic
- **Combination**: All filters are AND operations
- **Order**: tag filter → status filter → priority filter
- **Case-insensitive**: Tag filtering ignores case
- **Partial matching**: No (exact tag match required)

#### Examples
```bash
# List all todos
todo list

# List only pending todos
todo list --filter pending

# List high priority todos
todo list --priority HIGH

# List todos with specific tag
todo list --tag work

# Combined filters
todo list --filter pending --priority HIGH --tag urgent
```

#### Output Format

##### With Tags
```
42. [work, urgent] Complete project proposal
43. [personal] Buy groceries
44. [bug, critical] Fix login issue
```

##### Without Tags
```
42. Complete project proposal
43. Buy groceries
44. Fix login issue
```

##### With Priority and Due Date
```
42. [work, urgent] Complete project proposal (HIGH) - Due: 2026-05-10
43. [personal] Buy groceries (MEDIUM)
44. [bug, critical] Fix login issue (HIGH) - Due: 2026-05-05
```

#### Empty Results
```
No todos found matching the criteria.
```

### 3. Other Commands (Unchanged)

**Done Command**: `todo done <id>`
- No changes required
- Maintains existing behavior

**Delete Command**: `todo delete <id>`
- No changes required
- Maintains existing behavior

## Data Types

### Tag String
- **Type**: Unicode string
- **Encoding**: UTF-8
- **Length**: 1-20 characters
- **Validation**: Trimmed, non-empty, unique (case-insensitive)

### Date Format
- **Format**: YYYY-MM-DD
- **Example**: 2026-05-03
- **Validation**: Strict ISO date format

### Priority Enum
- **Values**: HIGH, MEDIUM, LOW
- **Case-sensitive**: Must be uppercase
- **Storage**: SQLAlchemy enum

## Error Handling Contract

### Validation Errors
All validation errors follow this pattern:
```
Error: <descriptive message>
```

### System Errors
Database or system errors:
```
Error: <technical description>
```

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation or business logic error |
| 2 | CLI argument parsing error |

## Backward Compatibility

### Guaranteed Compatibility
- **Existing commands**: All work without modification
- **Output format**: Untagged todos display identically
- **Filter behavior**: Existing filters work as before
- **Exit codes**: Same success/error codes

### New Behavior
- **Tagged todos**: Display with `[tag1, tag2]` prefix
- **New options**: `--tag` available on `add` and `list`
- **Validation**: Stricter input validation for tags

## Examples

### Complete Usage Scenarios

#### Scenario 1: Basic Workflow
```bash
# Add todos with tags
$ todo add "Review code changes" --tag work --tag review
Todo added successfully (ID: 1)

$ todo add "Call dentist" --tag personal --tag health
Todo added successfully (ID: 2)

# List all todos
$ todo list
1. [work, review] Review code changes
2. [personal, health] Call dentist

# Filter by tag
$ todo list --tag work
1. [work, review] Review code changes

# Filter by status
$ todo list --filter pending
1. [work, review] Review code changes
2. [personal, health] Call dentist
```

#### Scenario 2: Combined Filters
```bash
$ todo add "Fix critical bug" --priority HIGH --tag bug --tag urgent
Todo added successfully (ID: 3)

$ todo add "Write documentation" --priority MEDIUM --tag work
Todo added successfully (ID: 4)

# Filter by multiple criteria
$ todo list --filter pending --priority HIGH --tag urgent
3. [bug, urgent] Fix critical bug (HIGH)
```

#### Scenario 3: Error Handling
```bash
# Too many tags
$ todo add "Test todo" --tag 1 --tag 2 --tag 3 --tag 4 --tag 5 --tag 6
Error: Too many tags (max 5)

# Duplicate tags
$ todo add "Test todo" --tag work --tag Work
Error: Duplicate tag: 'Work'

# Long tag
$ todo add "Test todo" --tag this_is_a_very_long_tag_that_exceeds_the_limit
Error: Tag too long (max 20 chars): 'this_is_a_very_long_tag_that_exceeds_the_limit'
```

## Testing Contract

### CLI Integration Tests Required
- Tag validation (count, length, duplicates)
- Tag filtering (case-insensitive, combined filters)
- Output formatting (with/without tags)
- Error messages and exit codes
- Backward compatibility (existing commands)

### Sample Test Commands
```bash
# Valid tag operations
todo add "Test" --tag valid
todo list --tag valid
todo list --tag VALID  # Should find same todo

# Invalid operations
todo add "Test" --tag ""  # Empty tag
todo add "Test" --tag a --tag a  # Duplicate
todo add "Test" --tag this_tag_is_too_long_to_be_valid
```

## Future Extensions

### Potential Additions
- **Tag autocomplete**: Suggest existing tags
- **Tag statistics**: Show tag usage counts
- **Bulk tagging**: Tag multiple todos at once

### Contract Stability
This contract remains stable for the initial implementation. Future extensions will be added as separate contract versions.

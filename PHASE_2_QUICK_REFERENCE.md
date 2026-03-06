# Phase 2 Quick Reference Guide

## Access Stream Management

**URL**: `http://localhost:8000/school/headteacher/classes/`

## What You Can Do

### 1. **Create a Stream**
- Click "Manage Streams" button on any class
- Enter stream name (e.g., "A", "Science")
- Optionally enter code (e.g., "STR_A")
- Click "Add"
- Stream appears in list immediately

### 2. **Edit a Stream**
- Open stream management modal
- Click "Edit" on any stream
- Confirm new name in prompt
- Confirm new code in prompt
- Click OK
- Stream updates in list

### 3. **Delete a Stream**
- Open stream management modal
- Click "Delete" on any stream
- Confirm deletion dialog
- Stream removed from list
- ⚠️ Students in that stream will have stream assignment cleared

### 4. **View Stream Info**
- Stream count shown in table: "2 Streams"
- Existing streams list shows name and code
- Click class name in modal title to remind which class

## Features

✅ **AJAX-powered**: No page reload needed  
✅ **Real-time updates**: Changes visible immediately  
✅ **Error handling**: Duplicate streams prevented  
✅ **Input validation**: Stream name required  
✅ **School isolated**: Only manage your school's streams  

## Files Modified

- `schools/views.py` - Added stream CRUD logic
- `schools/templates/schools/classes.html` - Added UI and JavaScript
- No database changes needed (Stream model created in Phase 1)

## Testing URLs

- Classes page: `/school/headteacher/classes/`
- Load streams API: `/school/load-streams-for-class/?class_id=13`
- Admin panel: `/admin/schools/stream/`

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Name required" | Stream name is empty | Enter a stream name |
| "already exists in this class" | Stream name duplicate | Use different name |
| "Stream not found" | Deleted by another user | Refresh page |
| "Class not found" | Invalid class ID | Select valid class |
| Network error | Server down or timeout | Check server logs |

## Known Limitations

- Stream names are case-sensitive (A ≠ a)
- Cannot reorder streams (alphabetical by default)
- Deleting stream unlinks students (no cascade delete)
- Code field is optional (auto-generated if empty)

## What's Next?

After Phase 2 testing is complete, Phase 3 will:
- Add stream field to student admission/editing forms
- Load streams dynamically based on classroom selection
- Validate stream belongs to selected classroom
- Enable student assignment to streams

See STREAMS_IMPLEMENTATION.md for detailed Phase 3 roadmap.

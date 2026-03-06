# Streams Support Audit - SkulPlus System

**Date**: February 5, 2026  
**Goal**: Ensure the entire system properly supports classes having multiple streams.

---

## EXECUTIVE SUMMARY

Currently, **the system has NO Stream model** but streams are being used implicitly in merit lists by mapping gender to stream (Male='M', Female='W'). This is a fundamental limitation that needs to be addressed at the data model level.

**Key Finding**: The system treats streams as a derived field (from gender) rather than as a proper entity. This prevents:
1. Classes from having multiple independent streams
2. Stream-specific subject allocations
3. Stream-specific teacher assignments
4. Stream-level reporting and analysis

---

## FEATURE-BY-FEATURE AUDIT

### 1. ✅ MERIT LISTS (Partial - Uses Gender as Proxy)

**Current State**:
- Location: `schools/views.py` (lines 1909-2050+), `schools/templates/schools/merit_lists.html`
- Status: **PARTIALLY WORKING** - Uses gender as stream identifier
- Implementation: `stream = 'M' if student.gender == 'Male' else 'W'`

**Issues**:
- Cannot filter merit lists by actual streams
- Cannot have multiple streams within same gender
- Stream is cosmetic (display-only), not structural

**What Works**:
- Merit list displays STRM column with M/W values
- PDF and Excel exports include STRM column
- Grade distribution and class means are calculated

**What Doesn't Work**:
- Cannot select merit list by stream
- Cannot allocate subjects to specific streams
- Cannot assign teachers to specific streams
- Streams should be class-specific entities, not derived from gender

---

### 2. ❌ CLASS CREATION (No Stream Support)

**Location**: `schools/views.py` (lines 1512-1573), `schools/forms.py` (ClassRoomForm)

**Current Fields**:
- `name` (e.g., "Grade 5")
- `section` (e.g., "East", "West")
- `class_teacher`
- `order`

**Issues**:
- **No stream definition at class creation time**
- `section` field is being misused as a potential stream identifier but not formally
- No way to specify "Class 5 has streams A, B, C"
- Cannot set which subjects are available per stream
- Cannot set which teachers teach which streams

**What Should Happen**:
```python
# When creating "Grade 5", admin should be able to:
# - Define it has 3 streams: A, B, C
# - OR: Define streams by name
# - OR: Define streams inherit from a pattern
```

**Current Form Definition**:
```python
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'section', 'class_teacher']
```
❌ **No stream field**

---

### 3. ❌ ADDING STUDENTS (No Stream Assignment)

**Location**: `schools/views.py` (admit_student, admit_student_new, edit_student)

**Current Fields Assigned**:
- `classroom` (class only, no stream)
- `first_name`, `last_name`
- `gender`
- `admission_number`, `admission_date`
- `parent_info`

**Issues**:
- **Student has no `stream` field**
- When admitting student, cannot specify which stream they're in
- Students are tied to class but not to stream within class
- Dependent on gender for merit list stream identification

**StudentForm Definition**:
```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'classroom', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'admission_number', 'admission_date', 'parent_name', 'parent_phone', 'parent_user', 'photo'
        ]
```
❌ **No stream field**

**What Should Happen**:
- When creating/editing a student, select: Classroom + Stream
- Stream options should be dynamically loaded based on selected classroom

---

### 4. ❌ SUBJECT ALLOCATION (No Stream Filtering)

**Location**: `schools/views.py` (lines 1248-1500)

**Current Process**:
1. Select class
2. Select subject
3. Select students to allocate

**Issues**:
- **Subject allocation cannot be stream-specific**
- When selecting students, no stream filter available
- Cannot allocate "Math to Grade 5 Stream A only"
- Must allocate subjects to whole class at once

**Current View Logic**:
```python
def load_students_for_subject(request):
    # Gets students by class_id only, no stream filtering
    students_qs = Student.objects.filter(
        school=school,
        classroom_id=class_id  # No stream filter
    )
```

**What Should Happen**:
- Admin selects: Class → Stream → Subject
- System loads only students in that stream
- Allocation is stream-level, not class-level

---

### 5. ❌ TEACHER ASSIGNMENT (No Stream-Level Assignment)

**Location**: `schools/views.py` (lines 500-540), `allocate_teacher` view

**Current Process**:
1. Select teacher
2. Select subjects
3. Select classes (multiple choice)
4. Create TeacherAssignment records

**Issues**:
- **TeacherAssignment has no stream field**
- Teacher is assigned to subject + class globally
- Cannot assign teacher to specific streams within class
- When class has multiple streams, cannot specify which streams teacher teaches

**Current Model**:
```python
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('teacher', 'subject', 'classroom')
```
❌ **No stream field**

**What Should Happen**:
```python
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)
    # If stream is NULL, teacher teaches all streams in that class
```

---

### 6. ⚠️ MARKS ENTRY (Class-Level, Not Stream-Aware)

**Location**: `schools/views.py` (enter_marks_page, load_marks_students, save_marks)

**Current Process**:
1. Select exam, term
2. Select class
3. Select subject
4. Enter marks for all students in that class

**Issues**:
- **Cannot enter marks by stream**
- MarkSheet is tied to classroom, not to stream
- When class has multiple streams with same subject, must enter marks separately for each

**Current Model**:
```python
class MarkSheet(models.Model):
    term = models.CharField(max_length=20)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    school_class = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('exam', 'school_class', 'subject')
```
❌ **No stream field**

**What Should Happen**:
- MarkSheet should optionally be stream-specific
- Can create separate marksheets for same subject in different streams
- Or can create one marksheet and filter students by stream when entering marks

---

### 7. ⚠️ MARK ENTRY UI (Not Stream-Aware)

**Location**: `schools/views.py` load_marks_students function

**Current**:
```python
# Loads ALL students in the class, not filtered by stream
students_list = Student.objects.filter(school=school, classroom_id=class_id)
```

**Issue**: No option to filter/select stream

---

## MODEL REQUIREMENTS

To properly support streams, the system needs:

### NEW: Stream Model
```python
class Stream(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=50)  # e.g., "A", "B", "C" or "Science", "Arts"
    code = models.CharField(max_length=10)  # e.g., "STR_A", "STR_B"
    
    class Meta:
        unique_together = ('classroom', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.classroom.name} - Stream {self.name}"
```

### UPDATED: Student Model
```python
class Student(models.Model):
    # ... existing fields ...
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)  # NEW
    # ... rest of fields ...
```

### UPDATED: SubjectAllocation Model
```python
class SubjectAllocation(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='allocations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)  # NEW
    # ... rest of fields ...
```

### UPDATED: TeacherAssignment Model
```python
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)  # NEW
    # If stream is NULL, teacher teaches all streams in this class+subject
```

### OPTIONAL: MarkSheet Model Update
```python
class MarkSheet(models.Model):
    # ... existing fields ...
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)  # OPTIONAL
    # If NULL, marks are entered at class level but can be filtered by student stream
```

---

## IMPLEMENTATION ROADMAP

### PHASE 1: Data Model Setup (Backend Foundation)
1. ✅ Create Stream model
2. ✅ Add stream ForeignKey to Student
3. ✅ Add stream ForeignKey to SubjectAllocation
4. ✅ Add stream ForeignKey to TeacherAssignment
5. ✅ Create migration
6. ✅ Register Stream in admin.py
7. ✅ Update admin list displays to show streams

### PHASE 2: Class Management UI
1. Update ClassRoomForm to include stream creation
2. Create modal/form for adding streams to a class
3. Update classes_management view to handle stream CRUD
4. Update class display to show list of streams

### PHASE 3: Student Management UI
1. Update StudentForm to include stream field
2. Update admit_student_new view to load streams for selected class
3. Add JavaScript to dynamically load streams based on selected classroom
4. Update student list templates to show streams
5. Update edit_student to allow changing stream

### PHASE 4: Subject Allocation UI
1. Update subject_allocation view to include stream filtering
2. Add stream selection to the allocation form
3. Update load_students_for_subject to filter by stream
4. Update save_subject_allocations to handle stream
5. Add UI for bulk stream selection

### PHASE 5: Teacher Assignment UI
1. Update allocate_teacher view to include stream selection
2. Add stream multi-select to TeacherAllocationForm
3. Update UI to show stream options for each class
4. Update teacher assignment display to show streams

### PHASE 6: Marks Entry UI
1. Update enter_marks_page to offer stream filtering
2. Update load_marks_students to accept stream parameter
3. Filter student list by stream in mark entry
4. Update MarkSheet creation to optionally include stream

### PHASE 7: Reports & Exports
1. Update merit lists to filter by stream
2. Add stream-specific merit list generation
3. Update PDF/Excel exports to respect stream
4. Add stream column to all reports
5. Create stream-level analysis reports

### PHASE 8: Data Migration (if existing data)
1. Create data migration to set streams for existing students
2. Option 1: Use gender mapping (M → Stream A, W → Stream B)
3. Option 2: Manual mapping via admin interface
4. Option 3: Batch import with stream assignments

---

## PRIORITY MATRIX

| Feature | Complexity | Impact | Priority |
|---------|-----------|--------|----------|
| Stream Model + Migration | Low | Critical | 1 |
| Student Stream Assignment | Medium | Critical | 2 |
| Subject Allocation by Stream | Medium | High | 3 |
| Teacher Assignment by Stream | Medium | High | 4 |
| Merit Lists Stream Filtering | Low | High | 5 |
| Marks Entry Stream Filtering | Medium | Medium | 6 |
| Data Migration | High | Depends | 7 |

---

## CURRENT GAPS SUMMARY

| Area | Status | Issue |
|------|--------|-------|
| Data Model | ❌ Missing | No Stream entity |
| Student Stream | ❌ Missing | Can't assign stream to student |
| Class Streams | ❌ Missing | Can't define which streams exist in a class |
| Subject Allocation | ❌ Not Stream-Aware | All students in class allocated together |
| Teacher Assignment | ❌ Not Stream-Aware | Teacher assigned to class globally, not per-stream |
| Merit Lists | ⚠️ Partial | Uses gender as proxy, no real stream filtering |
| Marks Entry | ⚠️ Partial | No stream-level organization |
| Reports | ⚠️ Partial | Can display stream info but can't filter by it |

---

## DESIGN DECISION: Stream Naming

The system should support flexible stream naming:
- **Option A**: Single-character names (A, B, C, etc.)
- **Option B**: Descriptive names (Science, Arts, Commerce)
- **Option C**: Numeric names (1, 2, 3)
- **Recommendation**: Store both code (A, B) and descriptive name in Stream model

---

## BACKWARD COMPATIBILITY

Once Stream model is implemented:
1. Merit list 'stream' field (currently derived from gender) can be updated to use actual Stream data
2. Gender field remains for demographic purposes
3. Existing reports can be regenerated with proper streams
4. Export functionality enhanced but remains compatible

---

## NEXT STEPS

1. **Review this audit with development team**
2. **Approve Stream model design**
3. **Begin PHASE 1 implementation**
4. **Create Django migration for Stream model**
5. **Update forms and views incrementally**
6. **Add tests for stream-based filtering**

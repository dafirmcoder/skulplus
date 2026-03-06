(function(){

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const sourceClass = document.getElementById('sourceClass');
const targetClass = document.getElementById('targetClass');
const btnLoad = document.getElementById('btnLoad');
const btnPromoteSelected = document.getElementById('btnPromoteSelected');
const studentsTbody = document.querySelector('#studentsTable tbody');
const chkAll = document.getElementById('chkAll');

function togglePromoteBtn(){
  const any = document.querySelectorAll('.student-chk:checked').length > 0;
  btnPromoteSelected.disabled = !any || !targetClass.value;
}

chkAll && chkAll.addEventListener('change', ()=>{
  const chks = document.querySelectorAll('.student-chk');
  chks.forEach(c=> c.checked = chkAll.checked);
  togglePromoteBtn();
});

btnLoad.addEventListener('click', ()=>{
  const cid = sourceClass.value;
  if(!cid){ alert('Select a source class'); return; }
  fetch(LOAD_URL + '?class_id=' + cid, {credentials:'same-origin'})
    .then(r=>r.json()).then(data=>{
      const students = data.students || [];
      studentsTbody.innerHTML = '';
      if(students.length===0){
        studentsTbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#888">No students found</td></tr>';
        return;
      }
      students.forEach((s,i)=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><input type="checkbox" class="student-chk" value="${s.id}"></td>
          <td>${i+1}</td>
          <td>${s.name}</td>
          <td>${s.admission_number || ''}</td>
          <td>${s.gender || ''}</td>
          <td>
            <button class="btnPromote" data-id="${s.id}">Promote</button>
            <button class="btnDemote" data-id="${s.id}">Demote</button>
          </td>
        `;
        studentsTbody.appendChild(tr);
      });

      // wire up events
      document.querySelectorAll('.student-chk').forEach(c=> c.addEventListener('change', togglePromoteBtn));
      document.querySelectorAll('.btnPromote').forEach(b=> b.addEventListener('click', perStudentPromote));
      document.querySelectorAll('.btnDemote').forEach(b=> b.addEventListener('click', perStudentDemote));
      togglePromoteBtn();
    }).catch(err=>{ console.error(err); alert('Error loading students'); });
});

btnPromoteSelected.addEventListener('click', ()=>{
  const selected = Array.from(document.querySelectorAll('.student-chk:checked')).map(i=> parseInt(i.value));
  const target = parseInt(targetClass.value);
  if(selected.length===0){ alert('Select students first'); return; }
  if(!target){ alert('Select target class'); return; }
  if(!confirm(`Move ${selected.length} students to selected class?`)) return;
  fetch(MOVE_URL, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {'Content-Type':'application/json', 'X-CSRFToken': csrftoken},
    body: JSON.stringify({student_ids: selected, target_class_id: target})
  }).then(r=>r.json()).then(res=>{
    if(res.success){ alert('Moved '+res.moved+' students'); btnLoad.click(); }
    else alert('Error: '+(res.error||'unknown'));
  }).catch(err=>{ console.error(err); alert('Request failed'); });
});

// promote to next class (auto)
const btnPromoteNext = document.getElementById('btnPromoteNext');
if(btnPromoteNext){
  btnPromoteNext.addEventListener('click', ()=>{
    const selected = Array.from(document.querySelectorAll('.student-chk:checked')).map(i=> parseInt(i.value));
    if(selected.length===0) return alert('Select students');
    if(!confirm('Promote selected students to next class (or graduate if final)?')) return;
    fetch(PROMOTE_NEXT_URL, {method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken}, body: JSON.stringify({student_ids:selected})})
      .then(r=>r.json()).then(res=>{
        if(res.success){ alert(`Promoted ${res.moved} moved, ${res.graduated} graduated`); btnLoad.click(); }
        else alert('Error: '+(res.error||'unknown'));
      }).catch(err=>{console.error(err); alert('Request failed');});
  });
}

// undo last promotion
const btnUndo = document.getElementById('btnUndo');
if(btnUndo){
  btnUndo.addEventListener('click', ()=>{
    const selected = Array.from(document.querySelectorAll('.student-chk:checked')).map(i=> parseInt(i.value));
    if(selected.length===0) return alert('Select students');
    if(!confirm('Undo last promotion for selected students?')) return;
    fetch(UNDO_URL, {method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken}, body: JSON.stringify({student_ids:selected})})
      .then(r=>r.json()).then(res=>{ if(res.success){ alert('Undone: '+res.undone); btnLoad.click(); } else alert('Error'); }).catch(err=>{console.error(err); alert('Request failed');});
  });
}

// view logs
const btnLogs = document.getElementById('btnLogs');
if(btnLogs){
  btnLogs.addEventListener('click', ()=>{
    fetch(LOGS_URL, {credentials:'same-origin'}).then(r=>r.json()).then(data=>{
      const logs = data.logs || [];
      let txt = logs.map(l=> `${l.timestamp} - ${l.student_name}: ${l.from_class||'None'} -> ${l.to_class||'None'} by ${l.by||'?' } (${l.note})`).join('\n');
      alert(txt || 'No logs');
    }).catch(err=>{console.error(err); alert('Failed to fetch logs');});
  });
}

function perStudentPromote(e){
  const sid = parseInt(e.currentTarget.dataset.id);
  const target = parseInt(targetClass.value);
  if(!target){ alert('Select target class'); return; }
  fetch(MOVE_URL, {
    method: 'POST', credentials: 'same-origin', headers: {'Content-Type':'application/json', 'X-CSRFToken': csrftoken},
    body: JSON.stringify({student_ids: [sid], target_class_id: target})
  }).then(r=>r.json()).then(res=>{ if(res.success){ alert('Moved student'); btnLoad.click(); } else alert('Error: '+(res.error||'unknown')); }).catch(err=>{console.error(err); alert('Request failed');});
}

function perStudentDemote(e){
  const sid = parseInt(e.currentTarget.dataset.id);
  // auto-determine previous class then call move
  const source = sourceClass.value;
  if(!source){ alert('Select the source class first'); return; }
  fetch(ADJ_URL + '?class_id=' + source + '&direction=prev', {credentials:'same-origin'})
    .then(r=>r.json()).then(data=>{
      const target = data.id;
      if(!target){ alert('No previous class to demote to'); return; }
      if(!confirm('Move student to previous class?')) return;
      fetch(MOVE_URL, {
        method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
        body: JSON.stringify({student_ids:[sid], target_class_id: target})
      }).then(r=>r.json()).then(res=>{ if(res.success){ alert('Moved student'); btnLoad.click(); } else alert('Error: '+(res.error||'unknown')); }).catch(err=>{console.error(err); alert('Request failed');});
    }).catch(err=>{console.error(err); alert('Failed to determine previous class');});
}

})();

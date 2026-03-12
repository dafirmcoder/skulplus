(() => {
  const form = document.getElementById('schemeForm');
  if (!form) return;

  const topicSelect = document.getElementById('schemeTopic');
  const subtopicSelect = document.getElementById('schemeSubtopic');
  const subjectSelect = document.getElementById('schemeSubject');
  const generateBtn = document.getElementById('generateSchemeBtn');
  const loading = document.getElementById('schemeLoading');
  const previewBody = document.getElementById('schemePreviewBody');
  const downloadBtns = [document.getElementById('downloadSchemeBtn'), document.getElementById('downloadSchemeBtnTop')];
  const editBtns = [document.getElementById('editSchemeBtn'), document.getElementById('editSchemeBtnTop')];

  function setButtons(enabled){
    downloadBtns.forEach(btn => { if (btn) btn.disabled = !enabled; });
    editBtns.forEach(btn => { if (btn) btn.disabled = !enabled; });
  }

  async function loadTopics(subjectId){
    topicSelect.innerHTML = '<option value=\"\">Loading topics...</option>';
    topicSelect.disabled = true;
    subtopicSelect.innerHTML = '<option value=\"\">Select topic first</option>';
    subtopicSelect.disabled = true;
    if (!subjectId) return;
    try{
      const resp = await fetch(`/academics/ajax/topics/?subject_id=${subjectId}`);
      const data = await resp.json();
      topicSelect.innerHTML = '<option value=\"\">Select topic</option>';
      (data.topics || []).forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.title;
        topicSelect.appendChild(opt);
      });
      topicSelect.disabled = false;
    }catch(err){
      topicSelect.innerHTML = '<option value=\"\">Failed to load topics</option>';
      if (window.SkulPlusToast) SkulPlusToast('Unable to load topics', 'danger');
    }
  }

  async function loadSubtopics(topicId){
    subtopicSelect.innerHTML = '<option value=\"\">Loading subtopics...</option>';
    subtopicSelect.disabled = true;
    if (!topicId) return;
    try{
      const resp = await fetch(`/academics/ajax/subtopics/?topic_id=${topicId}`);
      const data = await resp.json();
      subtopicSelect.innerHTML = '<option value=\"\">Select subtopic</option>';
      (data.subtopics || []).forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.title;
        subtopicSelect.appendChild(opt);
      });
      subtopicSelect.disabled = false;
    }catch(err){
      subtopicSelect.innerHTML = '<option value=\"\">Failed to load subtopics</option>';
      if (window.SkulPlusToast) SkulPlusToast('Unable to load subtopics', 'danger');
    }
  }

  subjectSelect?.addEventListener('change', (e) => loadTopics(e.target.value));
  topicSelect?.addEventListener('change', (e) => loadSubtopics(e.target.value));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!subjectSelect.value || !topicSelect.value || !subtopicSelect.value) {
      if (window.SkulPlusToast) SkulPlusToast('Please complete all fields', 'warning');
      return;
    }
    loading?.classList.add('show');
    setTimeout(() => {
      loading?.classList.remove('show');
      previewBody.innerHTML = '';
      for (let i = 1; i <= 8; i += 1) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>Week ${i}</td>
          <td>—</td>
          <td>${topicSelect.options[topicSelect.selectedIndex].textContent}</td>
          <td>${subtopicSelect.options[subtopicSelect.selectedIndex].textContent}</td>
          <td>Activity ${i}</td>
          <td>Resource ${i}</td>
          <td>Assessment ${i}</td>
        `;
        previewBody.appendChild(tr);
      }
      setButtons(true);
      if (window.SkulPlusToast) SkulPlusToast('Scheme generated successfully', 'success');
    }, 1200);
  });
})();

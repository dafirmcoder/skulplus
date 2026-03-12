(() => {
  const form = document.getElementById('lessonWizard');
  if (!form) return;

  const steps = Array.from(form.querySelectorAll('.wizard-step'));
  const nextBtn = document.getElementById('nextStepBtn');
  const prevBtn = document.getElementById('prevStepBtn');
  const progress = document.getElementById('wizardProgress');
  const stepLabel = document.getElementById('wizardStep');
  const loading = document.getElementById('lessonLoading');

  let currentStep = 0;

  function showStep(index){
    steps.forEach((step, i) => {
      step.classList.toggle('active', i === index);
    });
    const pct = ((index + 1) / steps.length) * 100;
    if (progress) progress.style.width = `${pct}%`;
    if (stepLabel) stepLabel.textContent = `${index + 1}`;
    if (prevBtn) prevBtn.disabled = index === 0;
    if (nextBtn) nextBtn.textContent = index === steps.length - 1 ? 'Finish' : 'Continue';
  }

  function updateReview(){
    const cls = document.getElementById('lpClass');
    const subj = document.getElementById('lpSubject');
    const date = document.getElementById('lpDate');
    const length = document.getElementById('lpLength');
    const objectives = document.getElementById('lpObjectives');
    const activities = document.getElementById('lpActivities');
    const assessment = document.getElementById('lpAssessment');
    const reflection = document.getElementById('lpReflection');

    const overview = document.getElementById('reviewOverview');
    if (overview) {
      overview.innerHTML = `
        <li>Class: ${cls?.selectedOptions[0]?.textContent || '—'}</li>
        <li>Subject: ${subj?.selectedOptions[0]?.textContent || '—'}</li>
        <li>Date: ${date?.value || '—'}</li>
        <li>Duration: ${length?.value || '—'} mins</li>`;
    }
    const reviewObjectives = document.getElementById('reviewObjectives');
    if (reviewObjectives) reviewObjectives.textContent = objectives?.value || '—';
    const reviewActivities = document.getElementById('reviewActivities');
    if (reviewActivities) reviewActivities.textContent = activities?.value || '—';
    const reviewAssessment = document.getElementById('reviewAssessment');
    if (reviewAssessment) reviewAssessment.textContent = assessment?.value || '—';
    const reviewReflection = document.getElementById('reviewReflection');
    if (reviewReflection) reviewReflection.textContent = reflection?.value || '—';
  }

  nextBtn?.addEventListener('click', () => {
    if (currentStep < steps.length - 1) {
      currentStep += 1;
      if (currentStep === steps.length - 1) updateReview();
      showStep(currentStep);
    } else {
      updateReview();
      if (window.SkulPlusToast) SkulPlusToast('Lesson plan ready to generate', 'success');
    }
  });

  prevBtn?.addEventListener('click', () => {
    if (currentStep > 0) {
      currentStep -= 1;
      showStep(currentStep);
    }
  });

  document.getElementById('editLessonBtn')?.addEventListener('click', () => {
    currentStep = 0;
    showStep(currentStep);
  });

  document.getElementById('generateLessonBtn')?.addEventListener('click', () => {
    loading?.classList.add('show');
    setTimeout(() => {
      loading?.classList.remove('show');
      if (window.SkulPlusToast) SkulPlusToast('Lesson plan generated successfully', 'success');
    }, 1200);
  });

  showStep(currentStep);
})();

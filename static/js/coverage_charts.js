(() => {
  const data = window.coverageChartData || {};

  function buildPie() {
    const ctx = document.getElementById('completionPie');
    if (!ctx) return;
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'In Progress', 'Not Started'],
        datasets: [{
          data: data.pie || [60, 25, 15],
          backgroundColor: ['#16a34a', '#f59e0b', '#dc2626'],
          borderWidth: 0,
        }]
      },
      options: { plugins: { legend: { position: 'bottom' } } }
    });
  }

  function buildWeekly() {
    const ctx = document.getElementById('weeklyActivity');
    if (!ctx) return;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.weeklyLabels || ['W1','W2','W3','W4','W5'],
        datasets: [{
          label: 'Lessons',
          data: data.weekly || [4, 6, 5, 7, 3],
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37,99,235,0.15)',
          fill: true,
          tension: 0.3
        }]
      },
      options: { plugins: { legend: { display: false } } }
    });
  }

  function buildSubjectBar() {
    const ctx = document.getElementById('subjectCoverage');
    if (!ctx) return;
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.subjectLabels || ['Math', 'English', 'Science'],
        datasets: [{
          label: 'Coverage %',
          data: data.subjectCoverage || [65, 55, 40],
          backgroundColor: ['#16a34a', '#f59e0b', '#dc2626'],
          borderRadius: 8
        }]
      },
      options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }
    });
  }

  buildPie();
  buildWeekly();
  buildSubjectBar();
})();

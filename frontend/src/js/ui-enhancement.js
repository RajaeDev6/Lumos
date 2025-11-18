// UI Enhancements (frontend-only)
// - Adds chat assistant, file previews, AI timeline updates, charts and skeleton loaders
// - IMPORTANT: This script does NOT modify any backend calls, URLs, or existing functions.

(function(){
  // Helper: safe access to global state and DOM; run after main script
  function ready(fn){
    if (document.readyState === 'complete' || document.readyState === 'interactive'){
      setTimeout(fn, 0);
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  ready(() => {
    const stateRef = window.state || { syllabi: [], tests: [], plansGenerated: 0 };

    // --- AI Timeline ---
    const aiTimeline = document.getElementById('aiTimeline');
    const aiStatus = document.getElementById('aiStatus');
    if (aiTimeline) aiTimeline.classList.remove('hidden');

    function setTimelineStep(step){
      // step: 1..4
      const steps = aiTimeline.querySelectorAll('.step');
      steps.forEach((el, idx) => {
        if (idx < step) {
          el.querySelector('div').classList.remove('bg-gray-100','text-gray-500');
          el.querySelector('div').classList.add('bg-indigo-100','text-indigo-700');
        } else {
          el.querySelector('div').classList.add('bg-gray-100','text-gray-500');
          el.querySelector('div').classList.remove('bg-indigo-100','text-indigo-700');
        }
      });
    }

    // Initial step based on state
    setTimelineStep(stateRef.syllabi.length ? (stateRef.tests.length ? 3 : 2) : 1);

    // --- File Previews ---
    const filePreviewPanel = document.getElementById('filePreviewPanel');
    function addFilePreview(file, type){
      if (!filePreviewPanel) return;
      const card = document.createElement('div');
      card.className = 'file-preview';
      card.innerHTML = `
        <div class="flex items-start justify-between">
          <div>
            <div class="font-semibold text-sm">${file.name}</div>
            <div class="text-xs text-gray-500 mt-1">${(file.size/1024).toFixed(1)} KB • ${type.toUpperCase()}</div>
          </div>
          <div class="text-xs text-gray-400">${new Date().toLocaleTimeString()}</div>
        </div>
        <div class="mt-3 text-xs text-gray-600">
          Preview: ${file.type || 'n/a'}
        </div>
      `;
      filePreviewPanel.prepend(card);
    }

    // Hook into existing inputs without changing them
    const syllInput = document.getElementById('syllabusInput');
    const testInput = document.getElementById('testInput');
    if (syllInput) syllInput.addEventListener('change', (e)=>{ if(e.target.files[0]) addFilePreview(e.target.files[0],'syll'); aiStatus.textContent = 'Syllabus added'; setTimelineStep(2); });
    if (testInput) testInput.addEventListener('change', (e)=>{ if(e.target.files[0]) addFilePreview(e.target.files[0],'test'); aiStatus.textContent = 'Test added'; setTimelineStep(3); });

    // Also observe programmatic uploads simulated by existing code: watch state arrays periodically
    let lastCounts = { s: stateRef.syllabi.length, t: stateRef.tests.length };
    function animateNumberTo(el, target){
      if (!el) return;
      const start = parseInt(el.textContent || '0', 10) || 0;
      const end = parseInt(target || 0, 10);
      const duration = 700;
      const startTs = performance.now();
      function step(ts){
        const p = Math.min(1, (ts - startTs) / duration);
        const val = Math.floor(start + (end - start) * p);
        el.textContent = val;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    function updateProgressBars(s,t,p){
      const max = 5; // visual baseline
      const pS = Math.min(100, Math.round((s / max) * 100));
      const pT = Math.min(100, Math.round((t / max) * 100));
      const pP = Math.min(100, Math.round(((p||0) / Math.max(1,p || 1)) * 100));
      const elS = document.getElementById('progSyll'); if (elS) elS.style.width = pS + '%';
      const elT = document.getElementById('progTests'); if (elT) elT.style.width = pT + '%';
      const elP = document.getElementById('progPlans'); if (elP) elP.style.width = pP + '%';
    }

    function animateCounts(s,t,p){
      animateNumberTo(document.getElementById('statSyllabus'), s);
      animateNumberTo(document.getElementById('statTests'), t);
      animateNumberTo(document.getElementById('statPlans'), p || (window.state && window.state.plansGenerated) || 0);
      // also small summary counts in stats page
      animateNumberTo(document.getElementById('listSyllCount'), s);
      animateNumberTo(document.getElementById('listTestCount'), t);
      animateNumberTo(document.getElementById('listPlanCount'), (window.state && window.state.plansGenerated) || 0);
      updateProgressBars(s,t,p);
    }

    setInterval(()=>{
      const s = (window.state && window.state.syllabi) ? window.state.syllabi.length : 0;
      const t = (window.state && window.state.tests) ? window.state.tests.length : 0;
      const p = (window.state && window.state.plansGenerated) ? window.state.plansGenerated : 0;
      if (s !== lastCounts.s || t !== lastCounts.t){
        lastCounts = { s, t };
        aiStatus.textContent = (s>0 && t>0) ? 'Ready for AI analysis' : (s>0 ? 'Waiting for tests' : 'Waiting for syllabus');
        setTimelineStep(s? (t?4:2) : 1);
        renderCharts();
        animateCounts(s,t,p);
      }
    }, 900);

    // --- Plan Overview Observer to hide skeletons and show highlights ---
    const planOverview = document.getElementById('planOverview');
    if (planOverview){
      const mo = new MutationObserver((mutations) => {
        mutations.forEach(m => {
          if (m.type === 'characterData' || m.type === 'childList'){
            // new plan content appeared
            aiStatus.textContent = 'Plan generated';
            setTimelineStep(4);
            renderAIHighlights(planOverview.textContent || planOverview.innerText || '');
          }
        });
      });
      mo.observe(planOverview, { childList: true, subtree: true, characterData: true });
    }

    // --- AI Highlights / Heatmap ---
    function renderAIHighlights(text){
      // naive keyword extraction for demo (frontend-only)
      const keywords = ['Fractions','Algebra','Decimals','Review','Homework','Project'];
      const containerId = 'aiHighlights';
      let container = document.getElementById(containerId);
      if (!container){
        container = document.createElement('div');
        container.id = containerId;
        container.className = 'mt-4 p-4 bg-white rounded-lg border';
        const genResult = document.getElementById('generateResult');
        if (genResult) genResult.prepend(container);
      }
      const found = keywords.map(k => ({k,score: Math.min(1, (text.split(k).length-1) * 0.6)}));
      container.innerHTML = '<h4 class="font-bold mb-2">AI Tags & Weak Areas</h4>' +
        '<div class="flex gap-2 flex-wrap">' +
        found.map(f => `<div class="px-3 py-1 rounded-full text-sm ${f.score>0? 'bg-red-50 text-red-700':'bg-gray-100 text-gray-500'}" title="importance: ${f.score}">${f.k}</div>`).join('') +
        '</div>';

      // heatmap: simple bars
      let heat = document.getElementById('heatmap');
      if (!heat){
        heat = document.createElement('div'); heat.id='heatmap'; heat.className='mt-3 space-y-2'; container.appendChild(heat);
      }
      heat.innerHTML = found.map(f => `
        <div class="text-xs text-gray-600 flex justify-between"><div>${f.k}</div><div>${Math.round(f.score*100)}%</div></div>
        <div class="w-full bg-gray-100 rounded h-2 overflow-hidden"><div style="width:${Math.round(f.score*100)}%" class="h-2 bg-gradient-to-r from-red-400 to-yellow-300"></div></div>
      `).join('');
    }

    // --- Charts (Chart.js) ---
    let syllabusChart=null, testsChart=null;
    function renderCharts(){
      const ctxS = document.getElementById('chartSyllabus');
      const ctxT = document.getElementById('chartTests');
      const sCount = (window.state && window.state.syllabi) ? window.state.syllabi.length : 0;
      const tCount = (window.state && window.state.tests) ? window.state.tests.length : 0;

      try{
        if (ctxS){
          if (!syllabusChart){
            syllabusChart = new Chart(ctxS.getContext('2d'), {
              type: 'doughnut', data: { labels:['Uploaded','Missing'], datasets:[{ data:[sCount, Math.max(0, 5-sCount)], backgroundColor:['#6366f1','#e5e7eb'], borderWidth:0 }] }, options:{ plugins:{ legend:{display:false} }, cutout: '70%'}
            });
          } else { syllabusChart.data.datasets[0].data = [sCount, Math.max(0,5-sCount)]; syllabusChart.update(); }
        }
        if (ctxT){
          if (!testsChart){
            testsChart = new Chart(ctxT.getContext('2d'), {
              type: 'bar', data: { labels:['T1','T2','T3','T4'], datasets:[{ label:'Test count', data:[tCount, Math.max(0,tCount-1), Math.max(0,tCount-2), Math.max(0,tCount-3)], backgroundColor:'#06b6d4' }] }, options:{ indexAxis:'x', plugins:{ legend:{display:false} } }
            });
          } else { testsChart.data.datasets[0].data = [tCount, Math.max(0,tCount-1), Math.max(0,tCount-2), Math.max(0,tCount-3)]; testsChart.update(); }
        }
      }catch(e){ console.warn('Chart render error', e); }
    }
    renderCharts();

    // --- Skeleton loader demonstration on generate button click (non-intrusive) ---
    const genBtn = document.getElementById('generateBtn');
    const genResult = document.getElementById('generateResult');
    function showSkeleton(){
      if (!genResult) return;
      genResult.innerHTML = `<div class="p-5 bg-white rounded-lg"><div class="h-4 w-1/3 skeleton mb-3"></div><div class="skeleton h-3 w-full mb-2"></div><div class="skeleton h-3 w-full mb-2"></div><div class="skeleton h-3 w-3/4"></div></div>`;
    }
    if (genBtn){
      genBtn.addEventListener('click', () => { aiStatus.textContent = 'Analyzing...'; showSkeleton(); });
    }

    // When planOverview gets content, our mutation observer will render highlights and charts

    // --- Floating AI Assistant (frontend-only) ---
    const assistantBtn = document.createElement('button');
    assistantBtn.className = 'assistant-btn p-3 rounded-full bg-indigo-600 text-white shadow-lg focus:outline-none';
    assistantBtn.id = 'assistantBtn';
    assistantBtn.title = 'AI Assistant';
    assistantBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v6a2 2 0 01-2 2h-3l-3 3-3-3H4a2 2 0 01-2-2V5z"/></svg>';
    document.body.appendChild(assistantBtn);

    const panel = document.createElement('div'); panel.className='assistant-panel hidden bg-white rounded-lg'; panel.id='assistantPanel';
    panel.innerHTML = `
      <div class="header">
        <div class="flex items-center gap-2"><strong>AI Assistant</strong><span class="text-xs opacity-80">(local)</span></div>
        <button id="assistantClose" class="text-white/90">✕</button>
      </div>
      <div class="messages" id="assistantMessages"></div>
      <div class="composer">
        <input id="assistantInput" class="flex-1 p-2 border border-gray-200 rounded-md" placeholder="Ask about the plan (local only)" />
        <button id="assistantSend" class="px-3 py-1 bg-indigo-600 text-white rounded-md">Send</button>
      </div>
    `;
    document.body.appendChild(panel);

    const assistantPanel = document.getElementById('assistantPanel');
    const assistantMessages = document.getElementById('assistantMessages');
    const assistantInput = document.getElementById('assistantInput');

    function toggleAssistant(show){
      if (show){ assistantPanel.classList.remove('hidden'); assistantPanel.classList.add('flex','flex-col'); assistantBtn.classList.add('hidden'); }
      else { assistantPanel.classList.add('hidden'); assistantPanel.classList.remove('flex','flex-col'); assistantBtn.classList.remove('hidden'); }
    }

    assistantBtn.addEventListener('click', ()=> toggleAssistant(true));
    document.getElementById('assistantClose').addEventListener('click', ()=> toggleAssistant(false));

    // simple local message handling
    function appendMessage(text, isUser){
      const m = document.createElement('div'); m.className = 'assistant-bubble' + (isUser? ' user':''); m.textContent = text; assistantMessages.appendChild(m); assistantMessages.scrollTop = assistantMessages.scrollHeight;
    }
    document.getElementById('assistantSend').addEventListener('click', ()=>{
      const v = assistantInput.value.trim(); if(!v) return; appendMessage(v, true); assistantInput.value='';
      // Fake AI reply (no backend calls)
      setTimeout(()=>{ appendMessage('I can summarize the current plan or highlight weak areas. Try "summary" or "weak areas".', false); }, 700);
    });

    // Quick helper: when clicking downloadPlan, show timeline/preview hint (non-invasive)
    const downloadBtn = document.getElementById('downloadPlan');
    if (downloadBtn) downloadBtn.addEventListener('click', ()=>{ aiStatus.textContent='Preparing export (frontend simulated)'; setTimeout(()=> aiStatus.textContent='Ready', 900); });

    // initial small render
    renderCharts();

  });
})();

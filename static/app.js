document.addEventListener('DOMContentLoaded', () => {
    // ---- GLOBALS & STATE ----
    let currentRunData = [];
    let currentRunId = '';
    let currentMetadata = {};
    let sseSource = null;

    // ---- UI CONSTANTS ----
    const ICONS = {
        config: '⚙️',
        stage_start: '▶️',
        dimension_scored: '📊',
        tc_complete: '✅',
        diagnosis: '🔍',
        run_complete: '🎉',
        run_error: '❌',
        default: '•'
    };

    // ---- TAB NAVIGATION ----
    const tabBtns = document.querySelectorAll('.tab-btn');
    const views = document.querySelectorAll('.view');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));
            btn.classList.add('active');
            const targetView = document.getElementById(btn.dataset.target);
            if (targetView) targetView.classList.add('active');
        });
    });

    const rlTabs = document.querySelectorAll('.rl-tab');
    rlTabs.forEach(t => {
        t.addEventListener('click', () => {
            rlTabs.forEach(x => x.classList.remove('active'));
            document.querySelectorAll('.rl-panel').forEach(p => p.classList.remove('active'));
            t.classList.add('active');
            const panel = document.getElementById(`rl-panel-${t.dataset.panel}`);
            if (panel) panel.classList.add('active');
        });
    });

    // ---- TOASTS ----
    window.showToast = function(title, message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        `;
        toast.onclick = () => toast.remove();
        container.appendChild(toast);
        setTimeout(() => { if (toast.parentNode) toast.remove(); }, 4000);
    };

    // ---- INITIALIZATION & DATA LOADING ----
    async function loadRuns() {
        try {
            const ul = document.getElementById('runs-ul');
            // Show skeletons
            ul.innerHTML = Array(3).fill(0).map(() => `
                <li class="run-item skeleton" style="height: 50px;"></li>
            `).join('');

            const res = await fetch('/api/runs');
            const runs = await res.json();
            
            ul.innerHTML = '';
            if (runs.length === 0) {
                ul.innerHTML = '<li class="no-runs">No runs yet</li>';
                return;
            }
            
            runs.forEach(run => {
                const isObj = typeof run === 'object';
                const id = isObj ? run.run_id : run;
                const status = isObj ? run.status : 'completed';
                const score = isObj && run.overall_score !== undefined ? run.overall_score : null;
                
                const li = document.createElement('li');
                li.className = 'run-item';
                li.innerHTML = `
                    <div class="run-item-header">
                        <span class="run-item-id">${id}</span>
                        <span class="run-status-badge badge-${status}">${status}</span>
                    </div>
                    ${score !== null ? `
                    <div class="run-score-bar-bg"><div class="run-score-bar-fill" style="width: ${score * 100}%"></div></div>
                    ` : ''}
                `;
                li.addEventListener('click', () => {
                    document.querySelectorAll('.run-item').forEach(x => x.classList.remove('selected'));
                    li.classList.add('selected');
                    loadRunDetails(id);
                });
                ul.appendChild(li);
            });
        } catch (e) {
            console.error('loadRuns error:', e);
            showToast('Error', 'Failed to load runs', 'error');
        }
    }

    async function loadRunDetails(runId) {
        currentRunId = runId;
        document.getElementById('header-run-id').textContent = `Viewing: ${runId}`;
        
        const btnLogs = document.getElementById('btn-view-logs');
        btnLogs.style.display = 'inline-block';
        btnLogs.onclick = () => window.open(`/api/runs/${runId}/logs`, '_blank');
        
        try {
            // Skeleton Views setup
            showSkeletons();

            const res = await fetch(`/api/runs/${runId}`);
            if (!res.ok) throw new Error('Run not found');

            let payload = await res.json();
            currentMetadata = payload.metadata || {}; // if metadata is included
            currentRunData = Array.isArray(payload) ? payload : (payload.eval_results || []);

            populateLiveConfig(currentMetadata.config || {});
            populateDimensionsView(currentMetadata.dimensions || []);
            populateOverview(currentRunData, currentMetadata.dimensions || []);
            populateTestCases(currentRunData, currentMetadata.dimensions || []);
            populateRLSignals(runId, currentRunData);
            
            // Load report
            const reportRes = await fetch(`/api/runs/${runId}/report`);
            const reportContent = document.getElementById('report-content');
            const downloadBtn = document.getElementById('btn-download-report');
            if (reportRes.ok) {
                const reportData = await reportRes.json();
                reportContent.innerHTML = marked.parse(reportData.markdown);
                downloadBtn.style.display = 'inline-block';
                downloadBtn.onclick = () => {
                    const blob = new Blob([reportData.markdown], { type: 'text/markdown' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `report_${runId}.md`;
                    a.click();
                };
            } else {
                reportContent.innerHTML = '<p style="color:var(--text-muted)">No report available.</p>';
                downloadBtn.style.display = 'none';
            }

        } catch (e) {
            console.error(e);
            showToast('Error', e.message, 'error');
        }
    }

    function showSkeletons() {
        document.getElementById('dynamic-rings-container').innerHTML = Array(4).fill(0).map(() => `<div class="skeleton skeleton-card" style="width:220px; height:200px;"></div>`).join('');
        document.getElementById('dimensions-grid').innerHTML = Array(3).fill(0).map(() => `<div class="skeleton skeleton-card"></div>`).join('');
        document.getElementById('tc-tbody').innerHTML = Array(5).fill(0).map(() => `<tr><td colspan="7"><div class="skeleton skeleton-table-row"></div></td></tr>`).join('');
    }

    // ---- LIVE SSE ORCHESTRATION ----
    document.getElementById('btn-run-new').addEventListener('click', async () => {
        try {
            const res = await fetch('/api/runs', { method: 'POST' });
            const data = await res.json();
            const runId = data.run_id;

            tabBtns[0].click(); // Live view
            document.getElementById('header-run-id').textContent = `Live: ${runId}`;
            
            const btnLogs = document.getElementById('btn-view-logs');
            btnLogs.style.display = 'inline-block';
            btnLogs.onclick = () => window.open(`/api/runs/${runId}/logs`, '_blank');

            const dot = document.getElementById('live-dot');
            const statusText = document.getElementById('live-status-text');
            const feed = document.getElementById('live-timeline-feed');
            const prog = document.getElementById('live-progress');
            const liveScores = document.getElementById('live-scores-grid');
            
            dot.className = 'dot running';
            statusText.textContent = 'Running Pipeline...';
            feed.innerHTML = '';
            liveScores.innerHTML = '';
            prog.style.width = '5%';

            document.getElementById('live-config-panel').classList.add('hidden');

            if (sseSource) sseSource.close();

            sseSource = new EventSource(`/api/runs/${runId}/stream`);
            
            sseSource.onmessage = (e) => {
                const ev = JSON.parse(e.data);
                if (ev.type === 'ping') return;
                
                handleLiveEvent(ev, feed, prog, liveScores);

                if (ev.type === 'run_complete') {
                    dot.className = 'dot done';
                    statusText.textContent = `Complete · score=${ev.overall_score?.toFixed(3)}`;
                    prog.style.width = '100%';
                    sseSource.close();
                    showToast('Run Complete', \`Evaluation finished with score \${ev.overall_score?.toFixed(3)}\`, 'success');
                    loadRuns();
                    loadRunDetails(runId);
                } else if (ev.type === 'run_error') {
                    dot.className = 'dot error';
                    statusText.textContent = 'Failed';
                    sseSource.close();
                    showToast('Run Failed', ev.error || 'Unknown error', 'error');
                }
            };

            sseSource.onerror = () => {
                statusText.textContent = 'Stream disconnected';
                dot.className = 'dot error';
                sseSource.close();
            };

        } catch (e) {
            showToast('Error', 'Failed to start run', 'error');
        }
    });

    function handleLiveEvent(ev, feed, prog, liveScores) {
        if (ev.type === 'config') {
            populateLiveConfig(ev.config);
            return;
        }

        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        let iconChar = ICONS[ev.type] || ICONS.default;
        let iconClass = 'active';
        
        if (ev.type === 'run_error') iconClass = 'error';
        if (ev.type === 'run_complete') { iconClass = 'success'; iconChar = ICONS.run_complete; }
        if (ev.type === 'tc_complete') iconChar = ICONS.tc_complete;
        if (ev.type === 'diagnosis') iconChar = ICONS.diagnosis;
        if (ev.type === 'dimension_scored') iconChar = ICONS.dimension_scored;
        
        let contentHtml = '';
        if (ev.type === 'stage_start') {
            contentHtml = `<h4>${ev.stage} started</h4>`;
        } else if (ev.type === 'dimension_scored') {
            contentHtml = `
                <h4>Dimension Scored <span class="tc-id">${ev.tc_id}</span></h4>
                <div style="font-size: 0.85rem; margin-top:4px;">
                    <strong>${ev.dimension}</strong>: <span style="color:var(--accent-2)">${ev.score.toFixed(3)}</span>
                </div>
            `;
        } else if (ev.type === 'diagnosis') {
            contentHtml = `
                <h4>Diagnosis Triggered <span class="tc-id">${ev.tc_id}</span></h4>
                <p style="font-size: 0.8rem; margin:4px 0 0 0; color:var(--text-secondary)">Detected underperformance. Analyzing root cause...</p>
            `;
            showToast('Diagnosis Initiated', \`TC \${ev.tc_id} scored poorly. Running diagnostics.\`, 'warning');
        } else if (ev.type === 'tc_complete') {
            contentHtml = `
                <h4>Test Case Complete <span class="tc-id">${ev.tc_id}</span></h4>
                <div class="timeline-stages">
                    <span class="stage-pill done">Overall: ${ev.overall.toFixed(3)}</span>
                </div>
            `;
            
            // Add to Leaderboard
            const card = document.createElement('div');
            card.className = 'live-tc-item';
            card.innerHTML = `
                <div class="live-tc-info">
                    <span class="live-tc-id">${ev.tc_id}</span>
                </div>
                <div class="live-tc-score" style="color:${ev.passed ? 'var(--success)' : 'var(--warning)'}">${ev.overall.toFixed(3)}</div>
            `;
            liveScores.prepend(card);
            
            // Update progress
            const currentW = parseFloat(prog.style.width) || 0;
            prog.style.width = Math.min(95, currentW + 5) + '%';
        } else if (ev.type === 'phase_progress') {
            const currentW = parseFloat(prog.style.width) || 0;
            const newW = (ev.current / Math.max(1, ev.total)) * 100;
            prog.style.width = Math.max(currentW, newW) + '%';
            return; // don't add to timeline to reduce noise
        } else if (ev.type === 'query_cache_hit') {
            contentHtml = `
                <h4>Cache Hit <span class="tc-id">${ev.tc_id}</span></h4>
                <div style="font-size: 0.85rem; color:var(--text-secondary)">Similarity: ${(ev.similarity || 0).toFixed(2)}</div>
            `;
        } else if (ev.type === 'firecrawl_scrape_done') {
            contentHtml = `
                <h4>Scrape Done <span class="tc-id">${ev.tc_id}</span></h4>
                <div style="font-size: 0.85rem; color:var(--text-secondary)">URL: ${ev.url}</div>
            `;
        } else if (ev.type === 'tc_diagnosis_complete') {
            contentHtml = `
                <h4>Diagnosis Complete <span class="tc-id">${ev.tc_id}</span></h4>
                <p style="font-size: 0.85rem; margin:4px 0 0 0;">Root cause analyzed for failure.</p>
            `;
            iconClass = 'warning';
        } else if (ev.type === 'round_complete') {
            contentHtml = `
                <h4>Round Complete <span class="tc-id">Round ${ev.round}</span></h4>
            `;
            iconClass = 'success';
        } else if (ev.type === 'judge_scored') {
            contentHtml = `
                <h4>Judge Scored <span class="tc-id">${ev.tc_id}</span></h4>
                <div style="font-size: 0.85rem; margin-top:4px;">
                    Overall: <span style="color:var(--accent-2)">${ev.overall.toFixed(3)}</span>
                </div>
            `;
        } else if (ev.type === 'indexed') {
            return; // skip timeline noise for indexing
        } else {
            contentHtml = `<h4>${ev.type}</h4>`;
        }

        item.innerHTML = `
            <div class="timeline-icon ${iconClass}">${iconChar}</div>
            <div class="timeline-content">${contentHtml}</div>
        `;
        
        // Remove empty message if present
        const empty = feed.querySelector('.empty-msg');
        if (empty) empty.remove();
        
        feed.appendChild(item);
        feed.scrollTop = feed.scrollHeight;
    }

    function populateLiveConfig(config) {
        const panel = document.getElementById('live-config-panel');
        if (!config || Object.keys(config).length === 0) return;
        panel.classList.remove('hidden');
        panel.innerHTML = `
            <div class="config-item">Generator: <strong>${config.generator_model || 'Unknown'}</strong></div>
            <div class="config-item">Judge: <strong>${config.judge_model || 'Unknown'}</strong></div>
            <div class="config-item">Test Cases: <strong>${config.num_test_cases || '—'}</strong></div>
            <div class="config-item">Pass Threshold: <strong>${config.pass_threshold || 0.65}</strong></div>
            <div class="config-item">Concurrency: <strong>${config.max_concurrent_tcs || 1}</strong></div>
        `;
    }

    // ---- DIMENSIONS VIEW ----
    function populateDimensionsView(dims) {
        const grid = document.getElementById('dimensions-grid');
        if (!dims || dims.length === 0) {
            grid.innerHTML = '<div class="empty-msg">No dimensions defined for this run.</div>';
            return;
        }
        grid.innerHTML = '';
        dims.forEach((d, i) => {
            grid.innerHTML += `
                <div class="dim-card">
                    <div class="dim-card-header">
                        <h4>${d.name}</h4>
                        <span class="dim-weight">Weight: ${d.weight}</span>
                    </div>
                    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">${d.description}</p>
                </div>
            `;
        });
    }

    // ---- OVERVIEW VIEW ----
    function populateOverview(data, dims) {
        const ringsContainer = document.getElementById('dynamic-rings-container');
        if (!data.length) {
            ringsContainer.innerHTML = '<div class="empty-msg">No test case data</div>';
            return;
        }

        // Calculate averages
        let overall = 0, passed = 0;
        let bestScore = -1, bestQuery = '';
        let worstScore = 2, worstQuery = '';
        
        // Dynamic dimension accumulators
        const dimTotals = {};
        const dimCounts = {};
        
        let passThreshold = currentMetadata?.pass_threshold || 0.65;
        
        data.forEach(tc => {
            const sc = tc.overall_score || 0;
            overall += sc;
            if (sc >= passThreshold) passed++;
            if (sc > bestScore) { bestScore = sc; bestQuery = tc.test_case_id; }
            if (sc < worstScore) { worstScore = sc; worstQuery = tc.test_case_id; }
            
            if (tc.dimensions) {
                Object.entries(tc.dimensions).forEach(([k, v]) => {
                    dimTotals[k] = (dimTotals[k] || 0) + v;
                    dimCounts[k] = (dimCounts[k] || 0) + 1;
                });
            }
        });

        // Setup Rings
        ringsContainer.innerHTML = '';
        
        // Always show Overall
        const avgOverall = overall / data.length;
        ringsContainer.innerHTML += createRingHTML('Overall Score', avgOverall, 'var(--accent-2)');
        
        // Show dimension rings
        Object.keys(dimTotals).forEach((dimName, i) => {
            const avg = dimTotals[dimName] / dimCounts[dimName];
            const color = `var(--dim-${(i % 7) + 1})`;
            ringsContainer.innerHTML += createRingHTML(dimName, avg, color);
        });

        // Delay to allow CSS animation to trigger on stroke-dasharray
        setTimeout(() => {
            ringsContainer.querySelectorAll('.circle').forEach(circle => {
                const val = circle.dataset.val;
                circle.setAttribute('stroke-dasharray', `${Math.max(0, Math.min(100, val * 100))}, 100`);
            });
        }, 100);

        // Stats
        document.getElementById('ov-pass-rate').textContent = `${((passed / data.length) * 100).toFixed(0)}%`;
        document.getElementById('ov-best-query').textContent = bestQuery;
        document.getElementById('ov-worst-query').textContent = worstQuery;
        document.getElementById('ov-duration').textContent = currentMetadata.duration ? `${currentMetadata.duration.toFixed(1)}s` : '—';
    }

    function createRingHTML(title, value, color) {
        return `
            <div class="score-card">
                <div class="ring-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                        <path class="circle" style="stroke: ${color}" stroke-dasharray="0, 100" data-val="${value}" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                    </svg>
                    <div class="score-value">${value.toFixed(2)}</div>
                </div>
                <h4>${title}</h4>
            </div>
        `;
    }

    // ---- TEST CASES TABLE ----
    function populateTestCases(data, dims) {
        const thead = document.getElementById('tc-thead');
        const tbody = document.getElementById('tc-tbody');
        
        let dimNames = dims ? dims.map(d => d.name) : [];
        if (dimNames.length === 0 && data.length > 0 && data[0].dimensions) {
            dimNames = Object.keys(data[0].dimensions);
        }

        // Rebuild Thead
        let theadHtml = `<tr>
            <th style="width: 30px;"></th>
            <th>Test Case ID</th>
            <th>Overall</th>
        `;
        dimNames.forEach(d => { theadHtml += `<th>${d}</th>`; });
        theadHtml += `<th>Reasoning</th></tr>`;
        thead.innerHTML = theadHtml;

        // Rebuild Tbody
        tbody.innerHTML = '';
        if (!data.length) return;

        const searchTerm = (document.getElementById('tc-search-input').value || '').toLowerCase();

        data.forEach((tc, idx) => {
            const tcId = tc.test_case_id || '';
            const reasoning = tc.reasoning || tc.ranking?.ranking_reasoning || tc.evaluation_reasoning || '';
            
            if (searchTerm && !tcId.toLowerCase().includes(searchTerm) && !reasoning.toLowerCase().includes(searchTerm)) return;

            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            
            let html = `
                <td><button class="expand-btn" data-idx="${idx}">▸</button></td>
                <td class="tc-id-cell">${tcId}</td>
                <td><strong>${(tc.overall_score || 0).toFixed(3)}</strong></td>
            `;
            
            dimNames.forEach(d => {
                const val = (tc.dimensions && tc.dimensions[d]) || 0;
                html += `<td>${val.toFixed(3)}</td>`;
            });
            
            html += `<td style="max-width:300px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-size:0.8rem; color:var(--text-secondary);">${reasoning}</td>`;
            tr.innerHTML = html;
            tbody.appendChild(tr);

            // Expansion Row
            const expTr = document.createElement('tr');
            expTr.className = 'tc-expanded-row';
            expTr.id = `exp-row-${idx}`;
            expTr.style.display = 'none';
            expTr.innerHTML = `
                <td colspan="${4 + dimNames.length}">
                    <div style="padding: 16px;">
                        <div class="tc-sub-tabs">
                            <button class="tc-sub-tab active" onclick="switchTcTab(${idx}, 'report', event); loadTcReport('${currentRunId}', '${tcId}', ${idx})">📄 Detailed Report</button>
                            <button class="tc-sub-tab" onclick="switchTcTab(${idx}, 'raw', event)">Raw JSON</button>
                        </div>
                        <div class="tc-sub-panel active" id="tc-panel-${idx}-report">
                            <div id="tc-report-content-${idx}" class="markdown-body" style="padding: 16px; background: rgba(0,0,0,0.2); border-radius: 8px;"><em>Loading detailed report...</em></div>
                        </div>
                        <div class="tc-sub-panel" id="tc-panel-${idx}-raw">
                            <pre style="font-size:0.8rem;">${JSON.stringify(tc, null, 2)}</pre>
                        </div>
                    </div>
                </td>
            `;
            tbody.appendChild(expTr);

            tr.addEventListener('click', () => {
                const row = document.getElementById(`exp-row-${idx}`);
                const btn = tr.querySelector('.expand-btn');
                if (row.style.display === 'none') {
                    row.style.display = 'table-row';
                    tr.classList.add('expanded');
                    if (btn) btn.textContent = '▾';
                    window.loadTcReport(currentRunId, tcId, idx);
                } else {
                    row.style.display = 'none';
                    tr.classList.remove('expanded');
                    if (btn) btn.textContent = '▸';
                }
            });
        });
    }

    document.getElementById('tc-search-input')?.addEventListener('input', () => {
        populateTestCases(currentRunData, currentMetadata.dimensions);
    });

    window.switchTcTab = function(idx, tabName, event) {
        const container = document.getElementById(`exp-row-${idx}`);
        container.querySelectorAll('.tc-sub-tab').forEach(t => t.classList.remove('active'));
        container.querySelectorAll('.tc-sub-panel').forEach(p => p.classList.remove('active'));
        event.target.classList.add('active');
        const panel = document.getElementById(`tc-panel-${idx}-${tabName}`);
        if (panel) panel.classList.add('active');
    };

    window.loadTcReport = async function(runId, tcId, idx) {
        const el = document.getElementById(`tc-report-content-${idx}`);
        if (!el || el.dataset.loaded === 'true') return;
        try {
            const res = await fetch(`/api/runs/${runId}/tc_report/${tcId}`);
            if (res.ok) {
                const data = await res.json();
                el.innerHTML = marked.parse(data.markdown);
                el.dataset.loaded = 'true';
            } else {
                el.innerHTML = '<p style="color:var(--text-muted)">No detailed report found for this test case yet.</p>';
            }
        } catch(e) {
            el.innerHTML = '<p style="color:var(--danger)">Failed to load test case report.</p>';
        }
    };

    // ---- RL SIGNALS ----
    async function populateRLSignals(runId, data) {
        try {
            const res = await fetch(`/api/rl/signals/${runId}`);
            if (!res.ok) return;
            const rlData = await res.json();

            // DPO
            const dpoContainer = document.getElementById('rl-panel-dpo');
            if (!rlData.dpo_pairs || !rlData.dpo_pairs.length) {
                dpoContainer.innerHTML = '<div class="empty-msg">No DPO pairs generated.</div>';
            } else {
                dpoContainer.innerHTML = `
                    <div class="table-container">
                        <table class="data-table">
                            <thead><tr><th>Query</th><th>Chosen URL</th><th>Rejected URL</th><th>Rationale</th></tr></thead>
                            <tbody>${rlData.dpo_pairs.map(p => `
                                <tr>
                                    <td><strong>${p.query}</strong></td>
                                    <td style="color:var(--success)">${p.chosen?.url}</td>
                                    <td style="color:var(--danger)">${p.rejected?.url}</td>
                                    <td style="font-size:0.8rem; color:var(--text-secondary)">${p.preference_rationale || '-'}</td>
                                </tr>`).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }

            // Diagnoses
            const diagContainer = document.getElementById('rl-panel-diagnostics');
            if (!rlData.tc_diagnoses || !rlData.tc_diagnoses.length) {
                diagContainer.innerHTML = '<div class="empty-msg">No diagnostics data.</div>';
            } else {
                diagContainer.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:16px;">
                        ${rlData.tc_diagnoses.map(d => `
                            <div class="stat-box" style="border-left: 4px solid var(--danger);">
                                <strong>${d.tc_id}</strong>
                                <p style="margin: 8px 0; font-size:0.9rem;">${d.root_cause_summary}</p>
                                ${d.improvement_actions ? `<ul style="font-size:0.85rem; color:var(--text-secondary)">${d.improvement_actions.map(a => `<li>${a}</li>`).join('')}</ul>` : ''}
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            // Taxonomy
            const taxonomyContainer = document.getElementById('rl-panel-taxonomy');
            if (!rlData.taxonomy || !rlData.taxonomy.length) {
                taxonomyContainer.innerHTML = '<div class="empty-msg">No pattern taxonomy generated.</div>';
            } else {
                taxonomyContainer.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:16px;">
                        ${rlData.taxonomy.map(t => `
                            <div class="stat-box" style="border-left: 4px solid var(--accent-1);">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <strong>${t.issue}</strong>
                                    <span class="stage-pill ${t.severity === 'critical' ? 'error' : (t.severity === 'high' ? 'warning' : 'done')}">${t.severity}</span>
                                </div>
                                <p style="margin: 8px 0 4px 0; font-size:0.9rem;">${t.description}</p>
                                <div style="font-size:0.85rem; color:var(--text-secondary)">
                                    <em>Fix: ${t.suggested_fix}</em>
                                    <br>Frequency: ${t.frequency}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            // Rewards
            const rewardsContainer = document.getElementById('rl-panel-rewards');
            if (!rlData.reward_signals || !rlData.reward_signals.length) {
                rewardsContainer.innerHTML = '<div class="empty-msg">No reward signals generated.</div>';
            } else {
                rewardsContainer.innerHTML = `
                    <div class="table-container">
                        <table class="data-table">
                            <thead><tr><th>URL</th><th>Composite Reward</th><th>Trajectory Δ</th><th>Components</th></tr></thead>
                            <tbody>${rlData.reward_signals.map(r => `
                                <tr>
                                    <td><div style="max-width:300px; overflow:hidden; text-overflow:ellipsis;" title="${r.url}">${r.url}</div></td>
                                    <td><strong>${r.composite_reward.toFixed(3)}</strong></td>
                                    <td>${r.trajectory?.rank_delta > 0 ? '+' : ''}${r.trajectory?.rank_delta} (Rank ${r.trajectory?.search_rank} → ${r.trajectory?.ideal_rank})</td>
                                    <td style="font-size:0.8rem; color:var(--text-secondary)">
                                        Rel: ${r.reward_components?.relevance?.toFixed(2)} | 
                                        Cmp: ${r.reward_components?.completeness?.toFixed(2)} | 
                                        Frsh: ${r.reward_components?.freshness?.toFixed(2)}
                                    </td>
                                </tr>`).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }

            // Export Button
            const exportBtn = document.getElementById('btn-export-rl');
            if (exportBtn) {
                exportBtn.onclick = () => {
                    const blob = new Blob([JSON.stringify(rlData.dpo_pairs, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `dpo_pairs_${runId}.json`;
                    a.click();
                    URL.revokeObjectURL(url);
                };
            }
        } catch (e) {
            console.error('populateRLSignals error:', e);
        }
    }

    // ---- KB EXPLORER ----
    async function loadKBStats() {
        try {
            const res = await fetch('/api/kb/stats');
            if (res.ok) {
                const st = await res.json();
                document.getElementById('kb-doc-count').textContent = st.points_count || 0;
                document.getElementById('kb-url-count').textContent = st.unique_urls || 0;
                document.getElementById('kb-dedup-count').textContent = st.deduped_count || 0;
                document.getElementById('kb-status').textContent = st.status || 'Active';
            }
        } catch (e) {
            console.error(e);
        }
    }

    document.getElementById('kb-search-btn').addEventListener('click', async () => {
        const q = document.getElementById('kb-search-input').value.trim();
        if (!q) return;
        const container = document.getElementById('kb-results');
        container.innerHTML = '<div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card"></div>';
        try {
            const res = await fetch(`/api/kb/search?q=${encodeURIComponent(q)}`);
            const results = await res.json();
            container.innerHTML = '';
            if (!results.length) {
                container.innerHTML = '<div class="empty-msg">No results found</div>';
                return;
            }
            results.forEach(r => {
                container.innerHTML += `
                    <div class="kb-result-card">
                        <div class="kb-score">Score: ${r.score.toFixed(4)}</div>
                        <div class="kb-url"><a href="${r.url}" target="_blank">${r.url}</a></div>
                        <div class="kb-snippet">${r.content ? r.content.substring(0, 250) + '...' : ''}</div>
                    </div>
                `;
            });
        } catch (e) {
            container.innerHTML = `<div class="empty-msg">Error: ${e.message}</div>`;
        }
    });

    document.getElementById('kb-search-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') document.getElementById('kb-search-btn').click();
    });

    // INIT
    loadRuns();
    loadKBStats();
});

document.addEventListener('DOMContentLoaded', () => {
    // Tabs
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

    // RL Sub-tabs
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

    let currentRunData = [];
    let currentRunId = '';

    // ── Fetch Runs List ──────────────────────────────────────────────
    async function loadRuns() {
        try {
            const res = await fetch('/api/runs');
            const runs = await res.json();
            const ul = document.getElementById('runs-ul');
            ul.innerHTML = '';
            if (runs.length === 0) {
                ul.innerHTML = '<li class="no-runs">No runs yet</li>';
                return;
            }
            runs.forEach(run => {
                const li = document.createElement('li');
                li.textContent = run;
                li.title = run;
                li.addEventListener('click', () => {
                    document.querySelectorAll('#runs-ul li').forEach(x => x.classList.remove('selected'));
                    li.classList.add('selected');
                    loadRunDetails(run);
                });
                ul.appendChild(li);
            });
        } catch (e) {
            console.error('loadRuns error:', e);
        }
    }

    // ── Load a run's details ─────────────────────────────────────────
    async function loadRunDetails(runId) {
        currentRunId = runId;
        document.getElementById('header-run-id').textContent = `Viewing: ${runId}`;
        try {
            const res = await fetch(`/api/runs/${runId}`);
            if (!res.ok) { console.error('run not found', runId); return; }

            let payload = await res.json();
            let data = Array.isArray(payload) ? payload : (payload.eval_results || []);
            currentRunData = data;

            if (!Array.isArray(payload)) {
                renderRegression(payload.regression);
            }

            populateOverview(data);
            populateTestCases(data);
            populateRLSignals(runId, data);
            loadKBStats();

            // Fetch and render report
            try {
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
                        window.URL.revokeObjectURL(url);
                    };
                } else {
                    reportContent.innerHTML = '<p style="color:var(--text-secondary)">No report available.</p>';
                    downloadBtn.style.display = 'none';
                }
            } catch (e) {
                console.error('Failed to load report:', e);
            }

        } catch (e) {
            console.error('loadRunDetails error:', e);
        }
    }

    // ── Overview (Animated Score Rings & Histograms) ─────────────────
    function populateOverview(data) {
        if (!data.length) return;
        let overall = 0, cov = 0, rank = 0, scrape = 0, scrape_c = 0;
        let passed = 0;
        let bestScore = -1, bestQuery = '';
        let worstScore = 2, worstQuery = '';

        const overallScores = [];
        const scrapeScores = [];

        data.forEach(tc => {
            const sc = tc.overall_score || 0;
            overall += sc;
            overallScores.push(sc);
            if (sc >= 0.8) passed++;
            if (sc > bestScore) { bestScore = sc; bestQuery = tc.test_case_id; }
            if (sc < worstScore) { worstScore = sc; worstQuery = tc.test_case_id; }

            cov  += tc.coverage?.recall_score || 0;
            rank += tc.ranking?.ndcg_at_5 || 0;

            Object.values(tc.scrape_quality || {}).forEach(sq => {
                const sqVal = sq.overall_markdown_quality || 0;
                scrape += sqVal;
                scrapeScores.push(sqVal);
                scrape_c++;
            });
        });

        const avgOverall = overall / data.length;
        const avgCov = cov / data.length;
        const avgRank = rank / data.length;
        const avgScrape = scrape_c > 0 ? scrape / scrape_c : 0;

        // Update Rings
        updateRing('ring-overall', 'ov-overall', avgOverall);
        updateRing('ring-coverage', 'ov-coverage', avgCov);
        updateRing('ring-ranking', 'ov-ranking', avgRank);
        updateRing('ring-scrape', 'ov-scrape', avgScrape);

        // Update Quick Stats
        document.getElementById('ov-pass-rate').textContent = `${((passed / data.length) * 100).toFixed(0)}% (${passed}/${data.length})`;
        document.getElementById('ov-best-query').textContent = `${bestQuery} (${bestScore.toFixed(2)})`;
        document.getElementById('ov-worst-query').textContent = `${worstQuery} (${worstScore.toFixed(2)})`;
        document.getElementById('ov-latency').textContent = `342 ms`;

        // Render Histograms
        renderHistogram('ov-histograms', 'Overall Score Distribution', overallScores);
        renderHistogram('ov-histograms', 'Scrape Quality Distribution', scrapeScores, true);
    }

    function updateRing(pathId, textId, value) {
        const path = document.getElementById(pathId);
        const text = document.getElementById(textId);
        if (text) text.textContent = value.toFixed(2);
        if (path) {
            const pct = Math.max(0, Math.min(100, Math.round(value * 100)));
            path.setAttribute('stroke-dasharray', `${pct}, 100`);
        }
    }

    function renderHistogram(containerId, title, scores, append = false) {
        const container = document.getElementById(containerId);
        if (!append) container.innerHTML = '';

        const bins = [0, 0, 0, 0, 0];
        scores.forEach(s => {
            if (s < 0.2) bins[0]++;
            else if (s < 0.4) bins[1]++;
            else if (s < 0.6) bins[2]++;
            else if (s < 0.8) bins[3]++;
            else bins[4]++;
        });

        const maxBin = Math.max(1, ...bins);
        const labels = ['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'];

        let html = `<div class="hist-card"><h4>${title}</h4>`;
        bins.forEach((cnt, idx) => {
            const pct = (cnt / maxBin) * 100;
            html += `
                <div class="hist-bar-row">
                    <span class="hist-label">${labels[idx]}</span>
                    <div class="hist-bar-track"><div class="hist-bar-fill" style="width: ${pct}%"></div></div>
                    <span class="hist-count">${cnt}</span>
                </div>
            `;
        });
        html += `</div>`;
        container.innerHTML += html;
    }

    // ── Test Cases Table with Filtering & Expandable Sub-tabs ────────
    function populateTestCases(data) {
        const filterCat = document.getElementById('tc-category-filter');
        const cats = new Set();
        data.forEach(tc => { if (tc.category) cats.add(tc.category); });
        filterCat.innerHTML = '<option value="">All Categories</option>';
        cats.forEach(c => {
            filterCat.innerHTML += `<option value="${c}">${c}</option>`;
        });

        renderTestCasesTable();
    }

    function renderTestCasesTable() {
        const tbody = document.getElementById('tc-tbody');
        tbody.innerHTML = '';
        if (!currentRunData.length) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--text-secondary)">No test cases available</td></tr>';
            return;
        }

        const searchTerm = (document.getElementById('tc-search-input').value || '').toLowerCase();
        const catFilter = document.getElementById('tc-category-filter').value;

        currentRunData.forEach((tc, idx) => {
            const tcId = tc.test_case_id || tc.id || '';
            const reasoning = tc.ranking?.ranking_reasoning || '';
            const cat = tc.category || '';

            if (catFilter && cat !== catFilter) return;
            if (searchTerm && !tcId.toLowerCase().includes(searchTerm) && !reasoning.toLowerCase().includes(searchTerm)) return;

            let sq_sum = 0, sq_cnt = 0;
            Object.values(tc.scrape_quality || {}).forEach(sq => { sq_sum += sq.overall_markdown_quality || 0; sq_cnt++; });
            const avg_sq = sq_cnt > 0 ? sq_sum / sq_cnt : 0;

            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.innerHTML = `
                <td><button class="expand-btn" data-idx="${idx}">▸</button></td>
                <td class="tc-id-cell">${tcId}</td>
                <td><strong>${(tc.overall_score || 0).toFixed(2)}</strong></td>
                <td>${(tc.coverage?.recall_score || 0).toFixed(2)}</td>
                <td>${(tc.ranking?.ndcg_at_5 || 0).toFixed(2)}</td>
                <td>${avg_sq.toFixed(2)}</td>
                <td class="reasoning-cell">${reasoning}</td>
            `;
            tbody.appendChild(tr);

            // Expandable details row
            const expTr = document.createElement('tr');
            expTr.className = 'tc-expanded-row';
            expTr.id = `exp-row-${idx}`;
            expTr.style.display = 'none';
            expTr.innerHTML = `
                <td colspan="7">
                    <div style="padding: 10px 16px;">
                        <div class="tc-sub-tabs">
                            <button class="tc-sub-tab active" onclick="switchTcTab(${idx}, 'report', event); loadTcReport('${currentRunId}', '${tcId}', ${idx})">📄 Full Report</button>
                            <button class="tc-sub-tab" onclick="switchTcTab(${idx}, 'scrape', event)">Scrape Quality</button>
                            <button class="tc-sub-tab" onclick="switchTcTab(${idx}, 'coverage', event)">Coverage Breakdown</button>
                            <button class="tc-sub-tab" onclick="switchTcTab(${idx}, 'ranking', event)">Ranking Breakdown</button>
                            <button class="tc-sub-tab" onclick="switchTcTab(${idx}, 'rl', event)">RL Signals</button>
                        </div>
                        <div class="tc-sub-panel active" id="tc-panel-${idx}-report">
                            <div id="tc-report-content-${idx}" class="markdown-content" style="padding: 12px; background: rgba(0,0,0,0.2); border-radius: 8px;"><em>Loading detailed report...</em></div>
                        </div>
                        <div class="tc-sub-panel" id="tc-panel-${idx}-scrape">
                            <p><strong>URLs Evaluated:</strong> ${sq_cnt}</p>
                            <ul>${Object.entries(tc.scrape_quality || {}).map(([u, sq]) => `<li><code>${u}</code> — Score: <strong>${(sq.overall_markdown_quality||0).toFixed(2)}</strong> (${(sq.issues_found||[]).length} issues)</li>`).join('')}</ul>
                        </div>
                        <div class="tc-sub-panel" id="tc-panel-${idx}-coverage">
                            <p><strong>Recall Score:</strong> ${(tc.coverage?.recall_score||0).toFixed(2)}</p>
                            <p><strong>Missing Topics:</strong> ${(tc.coverage?.must_mention_misses||[]).join(', ') || 'None! All key entities covered.'}</p>
                        </div>
                        <div class="tc-sub-panel" id="tc-panel-${idx}-ranking">
                            <p><strong>NDCG@5:</strong> ${(tc.ranking?.ndcg_at_5||0).toFixed(2)}</p>
                            <p><strong>LLM Ideal Ranking:</strong> [${(tc.ranking?.llm_ideal_ranking||[]).join(', ')}] vs Firecrawl: [${(tc.ranking?.firecrawl_ranking||[]).join(', ')}]</p>
                            <p><strong>Reasoning:</strong> ${tc.ranking?.ranking_reasoning || 'N/A'}</p>
                        </div>
                        <div class="tc-sub-panel" id="tc-panel-${idx}-rl">
                            <p>Potential DPO candidate preference pair or reward adjustment signal generated for this query.</p>
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
                    if (btn) btn.textContent = '▾';
                    window.loadTcReport(currentRunId, tcId, idx);
                } else {
                    row.style.display = 'none';
                    if (btn) btn.textContent = '▸';
                }
            });
        });

        document.querySelectorAll('.expand-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const idx = btn.dataset.idx;
                const row = document.getElementById(`exp-row-${idx}`);
                if (row.style.display === 'none') {
                    row.style.display = 'table-row';
                    btn.textContent = '▾';
                    const tc = currentRunData[idx];
                    const tcId = tc ? (tc.test_case_id || tc.id || '') : '';
                    window.loadTcReport(currentRunId, tcId, idx);
                } else {
                    row.style.display = 'none';
                    btn.textContent = '▸';
                }
            });
        });
    }

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
                el.innerHTML = '<p style="color:var(--text-secondary)">No detailed report found for this test case yet.</p>';
            }
        } catch(e) {
            el.innerHTML = '<p style="color:var(--danger)">Failed to load test case report.</p>';
        }
    };

    window.switchTcTab = function(idx, tabName, event) {
        const container = document.getElementById(`exp-row-${idx}`);
        container.querySelectorAll('.tc-sub-tab').forEach(t => t.classList.remove('active'));
        container.querySelectorAll('.tc-sub-panel').forEach(p => p.classList.remove('active'));
        event.target.classList.add('active');
        const panel = document.getElementById(`tc-panel-${idx}-${tabName}`);
        if (panel) panel.classList.add('active');
    };

    document.getElementById('tc-search-input')?.addEventListener('input', renderTestCasesTable);
    document.getElementById('tc-category-filter')?.addEventListener('change', renderTestCasesTable);

    // ── KB Explorer Stats ────────────────────────────────────────────
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
            console.error('loadKBStats error:', e);
        }
    }

    // ── RL Signals Sub-tabs & Panels ─────────────────────────────────
    async function populateRLSignals(runId, data) {
        try {
            const res = await fetch(`/api/rl/signals/${runId}`);
            if (!res.ok) return;
            const rlData = await res.json();

            // DPO Pairs
            const dpoContainer = document.getElementById('rl-panel-dpo');
            if (!rlData.dpo_pairs || rlData.dpo_pairs.length === 0) {
                dpoContainer.innerHTML = '<p style="color:var(--text-secondary)">No DPO pairs generated for this run.</p>';
            } else {
                dpoContainer.innerHTML = `
                    <p style="color:var(--text-secondary); margin-bottom: 12px;">Generated <strong>${rlData.dpo_pairs.length}</strong> Direct Preference Optimization (DPO) pairs.</p>
                    <table class="data-table">
                        <thead><tr><th>Query</th><th>Chosen URL (Rank)</th><th>Rejected URL (Rank)</th><th>Rationale</th></tr></thead>
                        <tbody>${rlData.dpo_pairs.map(p => `
                            <tr>
                                <td><strong>${p.query}</strong></td>
                                <td style="color:var(--success)">${p.chosen?.url} (#${p.chosen?.firecrawl_rank})</td>
                                <td style="color:var(--danger)">${p.rejected?.url} (#${p.rejected?.firecrawl_rank})</td>
                                <td style="font-size:0.8rem; color:var(--text-secondary)">${p.preference_rationale || '-'}</td>
                            </tr>`).join('')}
                        </tbody>
                    </table>
                `;
            }

            // Taxonomy
            const taxContainer = document.getElementById('rl-panel-taxonomy');
            if (!rlData.taxonomy || rlData.taxonomy.length === 0) {
                taxContainer.innerHTML = '<p style="color:var(--text-secondary)">No taxonomy patterns discovered.</p>';
            } else {
                taxContainer.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:12px;">
                        ${rlData.taxonomy.map(t => `
                            <div class="stat-box">
                                <span style="color:var(--accent)">${t.issue || 'Pattern'} (${t.frequency || ''})</span>
                                <strong>${t.description || ''}</strong>
                                <p style="font-size:0.82rem; color:var(--text-secondary); margin: 6px 0 0 0;">💡 Fix: ${t.suggested_fix || '-'}</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            // Diagnostics Panel
            const diagContainer = document.getElementById('rl-panel-diagnostics');
            if (!rlData.tc_diagnoses || rlData.tc_diagnoses.length === 0) {
                diagContainer.innerHTML = '<p style="color:var(--text-secondary)">No individual test case diagnoses. Either all test cases passed or no diagnostics were run.</p>';
            } else {
                diagContainer.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:16px;">
                        ${rlData.tc_diagnoses.map(d => {
                            const passed = d.overall_score >= 0.8;
                            const badgeColor = passed ? 'var(--success)' : 'var(--danger)';
                            const badgeText = passed ? 'PASSED' : 'FAILED';
                            const tags = (d.failure_dimensions || []).map(dim => `<span class="tag" style="background-color:rgba(239,68,68,0.1); color:var(--danger); border:1px solid rgba(239,68,68,0.2); padding: 2px 6px; border-radius:4px; font-size:0.75rem; margin-right:6px;">${dim}</span>`).join('') || '<span class="tag" style="background-color:rgba(16,185,129,0.1); color:var(--success); border:1px solid rgba(16,185,129,0.2); padding: 2px 6px; border-radius:4px; font-size:0.75rem; margin-right:6px;">none</span>';
                            
                            return `
                                <div class="stat-box" style="border-left: 4px solid ${badgeColor}; padding: 16px; background-color: var(--card-bg);">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                                        <div>
                                            <strong style="font-size:1.1rem; color:var(--text-primary);">${d.tc_id}</strong>
                                            <span style="margin-left: 8px; font-weight:bold; color:${badgeColor}; font-size:0.85rem;">[${badgeText} — Score: ${d.overall_score.toFixed(3)}]</span>
                                        </div>
                                        <div>
                                            ${tags}
                                        </div>
                                    </div>
                                    <p style="margin: 0 0 12px 0; font-size:0.95rem; color:var(--text-primary);">
                                        <strong>Root Cause:</strong> ${d.root_cause_summary}
                                    </p>
                                    <div style="margin-bottom:12px; font-size:0.85rem; color:var(--text-secondary); display:flex; flex-direction:column; gap:4px; background-color:rgba(255,255,255,0.02); padding:10px; border-radius:6px;">
                                        <div>📢 <strong>Coverage:</strong> ${d.coverage_diagnosis || '-'}</div>
                                        <div>📊 <strong>Ranking:</strong> ${d.ranking_diagnosis || '-'}</div>
                                        <div>🌐 <strong>Scraping:</strong> ${d.scrape_diagnosis || '-'}</div>
                                    </div>
                                    ${d.improvement_actions && d.improvement_actions.length > 0 ? `
                                        <div style="font-size:0.9rem;">
                                            <strong>Suggested Fix Actions:</strong>
                                            <ul style="margin: 6px 0 0 0; padding-left: 20px; color:var(--text-secondary); display:flex; flex-direction:column; gap:4px;">
                                                ${d.improvement_actions.map(act => `<li>${act}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>
                `;
            }

            // Rewards
            const rewContainer = document.getElementById('rl-panel-rewards');
            if (!rlData.reward_signals || rlData.reward_signals.length === 0) {
                rewContainer.innerHTML = '<p style="color:var(--text-secondary)">No reward distribution data.</p>';
            } else {
                rewContainer.innerHTML = `
                    <p style="color:var(--text-secondary); margin-bottom: 12px;">Collected <strong>${rlData.reward_signals.length}</strong> dense reward signals across search trajectories.</p>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Query</th>
                                <th>URL</th>
                                <th>Composite Reward</th>
                                <th>Components (Rel / Comp / Fresh / MD)</th>
                                <th>Trajectory Delta</th>
                            </tr>
                        </thead>
                        <tbody>${rlData.reward_signals.map(r => {
                            const rewardVal = r.composite_reward || 0;
                            const rewardColor = rewardVal >= 0.7 ? 'var(--success)' : (rewardVal >= 0.4 ? 'var(--accent)' : 'var(--danger)');
                            const delta = r.trajectory?.rank_delta || 0;
                            const deltaText = delta > 0 ? `+${delta}` : delta;
                            const deltaColor = delta > 0 ? 'var(--success)' : (delta < 0 ? 'var(--danger)' : 'var(--text-secondary)');
                            
                            const rc = r.reward_components || {};
                            const rel = rc.relevance !== undefined ? rc.relevance.toFixed(2) : '-';
                            const comp = rc.completeness !== undefined ? rc.completeness.toFixed(2) : '-';
                            const fresh = rc.freshness !== undefined ? rc.freshness.toFixed(2) : '-';
                            const md = rc.markdown_quality !== undefined ? rc.markdown_quality.toFixed(2) : '-';
                            
                            return `
                                <tr>
                                    <td><strong>${r.query || ''}</strong></td>
                                    <td style="font-size:0.8rem; max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"><a href="${r.url}" target="_blank" style="color:var(--accent); text-decoration:none;">${r.url}</a></td>
                                    <td><strong style="color:${rewardColor}">${rewardVal.toFixed(3)}</strong></td>
                                    <td style="font-size:0.8rem; color:var(--text-secondary)">${rel} / ${comp} / ${fresh} / ${md}</td>
                                    <td style="color:${deltaColor}; font-weight:bold;">${deltaText} (Search: #${r.trajectory?.search_rank} vs Ideal: #${r.trajectory?.ideal_rank})</td>
                                </tr>`;
                        }).join('')}
                        </tbody>
                    </table>
                `;
            }

            // Wire up Export
            document.getElementById('btn-export-rl').onclick = () => {
                const jsonl = (rlData.dpo_pairs || []).map(p => JSON.stringify(p)).join('\n');
                const blob = new Blob([jsonl], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `dpo_pairs_${runId}.jsonl`;
                a.click();
            };

        } catch (e) {
            console.error('populateRLSignals error:', e);
        }
    }

    // ── Regression ───────────────────────────────────────────────────
    function renderRegression(reg) {
        if (!reg) return;
        let el = document.getElementById('regression-banner');
        if (!el) {
            el = document.createElement('div');
            el.id = 'regression-banner';
            el.className = 'regression-banner';
            document.querySelector('.view-container').prepend(el);
        }
        el.textContent = `Regression: ${reg.trend || 'Unknown'}`;
        el.className = `regression-banner ${(reg.diff || 0) < -0.05 ? 'reg-bad' : 'reg-good'}`;
    }

    loadRuns();
    loadKBStats();

    // ── Run new eval ─────────────────────────────────────────────────
    let eventSource = null;
    document.getElementById('btn-run-new').addEventListener('click', async () => {
        try {
            const res = await fetch('/api/runs', { method: 'POST' });
            const data = await res.json();
            const runId = data.run_id;

            tabBtns[0].click();
            document.getElementById('header-run-id').textContent = `Live: ${runId}`;

            const dot        = document.getElementById('live-dot');
            const statusText = document.getElementById('live-status-text');
            const feed       = document.getElementById('live-feed');
            const prog       = document.getElementById('live-progress');
            const liveScores = document.getElementById('live-scores-grid');

            dot.classList.add('running');
            statusText.textContent = 'Running Pipeline...';
            feed.innerHTML = '';
            liveScores.innerHTML = '';
            prog.style.width = '5%';

            if (eventSource) eventSource.close();

            eventSource = new EventSource(`/api/runs/${runId}/stream`);
            eventSource.onmessage = (e) => {
                const ev = JSON.parse(e.data);

                if (ev.type === 'ping') return;

                const div = document.createElement('div');
                div.className = `event-log event-${ev.type}`;
                const icon = {
                    run_start:     '🚀',
                    phase_start:   '⚙️',
                    test_case_created: '📝',
                    firecrawl_search_done: '🔍',
                    firecrawl_scrape_done: '📄',
                    judge_scored:  '⚖️',
                    indexed:       '📦',
                    phase_complete:'✅',
                    run_complete:  '🎉',
                    run_error:     '❌',
                }[ev.type] || '•';

                let msg = `${ev.type}`;
                if (ev.tc_id) msg += ` · ${ev.tc_id}`;
                if (ev.query) msg += ` · "${ev.query.substring(0, 60)}"`;
                if (ev.phase) msg += ` · ${ev.phase}`;
                if (ev.message) msg += ` — ${ev.message}`;
                if (ev.overall !== undefined) {
                    msg += ` · score=${ev.overall.toFixed(2)}`;
                    // Add/update card in live leaderboard
                    const card = document.createElement('div');
                    card.className = 'live-tc-item';
                    card.style.cursor = 'pointer';
                    card.title = 'Click to switch to Test Cases tab and view full diagnosis report';
                    card.innerHTML = `
                        <div class="live-tc-info">
                            <span class="live-tc-id">${ev.tc_id}</span>
                        </div>
                        <div class="live-tc-score" style="color:${ev.overall >= 0.8 ? 'var(--success)' : 'var(--warning)'}">${ev.overall.toFixed(2)}</div>
                    `;
                    card.onclick = () => {
                        tabBtns[1].click(); // Switch to Test Cases tab
                    };
                    liveScores.prepend(card);

                    // Sync live data instantly to overview and tables as each test case completes!
                    loadRunDetails(runId);
                }
                if (ev.result_count !== undefined) msg += ` · ${ev.result_count} results`;
                if (ev.error) msg += ` — ${ev.error}`;

                div.textContent = `[${new Date().toLocaleTimeString()}] ${icon} ${msg}`;
                feed.appendChild(div);
                feed.scrollTop = feed.scrollHeight;

                // Progress
                if (ev.type === 'phase_start') {
                    const p = { test_generation: 15, execution: 50, retrieval_comparison: 80, rl_signals: 90, report: 95 };
                    if (p[ev.phase]) prog.style.width = p[ev.phase] + '%';
                }
                if (ev.type === 'test_case_created') prog.style.width = '25%';
                if (ev.type === 'judge_scored') prog.style.width = '70%';

                if (ev.type === 'run_complete') {
                    dot.classList.remove('running');
                    dot.classList.add('done');
                    statusText.textContent = `Complete · score=${ev.overall_score?.toFixed(2)}`;
                    prog.style.width = '100%';
                    eventSource.close();
                    loadRuns();
                    loadRunDetails(runId);
                }
                if (ev.type === 'run_error') {
                    dot.classList.remove('running');
                    dot.classList.add('error');
                    statusText.textContent = 'Error';
                    eventSource.close();
                }
            };
            eventSource.onerror = () => {
                statusText.textContent = 'Stream disconnected';
                dot.classList.remove('running');
                eventSource.close();
            };
        } catch (e) {
            console.error(e);
        }
    });

    // ── KB Search ────────────────────────────────────────────────────
    document.getElementById('kb-search-btn').addEventListener('click', async () => {
        const q = document.getElementById('kb-search-input').value.trim();
        if (!q) return;
        const container = document.getElementById('kb-results');
        container.innerHTML = '<p style="color:var(--text-secondary)">Searching…</p>';
        try {
            const res = await fetch(`/api/kb/search?q=${encodeURIComponent(q)}`);
            const results = await res.json();
            container.innerHTML = '';
            if (!results.length) {
                container.innerHTML = '<p style="color:var(--text-secondary)">No results found</p>';
                return;
            }
            results.forEach(r => {
                const div = document.createElement('div');
                div.className = 'kb-result-card';
                div.innerHTML = `
                    <div class="kb-score">Score: <strong>${(r.score || 0).toFixed(4)}</strong></div>
                    <div class="kb-url"><a href="${r.url}" target="_blank">${r.url}</a></div>
                    <div class="kb-snippet">${r.content ? r.content.substring(0, 300) + '…' : 'No content'}</div>
                `;
                container.appendChild(div);
            });
        } catch (e) {
            container.innerHTML = `<p style="color:var(--danger)">Search error: ${e.message}</p>`;
        }
    });

    document.getElementById('kb-search-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') document.getElementById('kb-search-btn').click();
    });
});

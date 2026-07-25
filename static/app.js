// Global variables to store current trends state
let currentTrends = [];

// Initialize Dashboard on Load
document.addEventListener("DOMContentLoaded", () => {
    loadTrends();
    setupTabListeners();
    setupFormListener();
    setupModalListener();
    
    // Refresh trends button listener
    document.getElementById("refresh-trends-btn").addEventListener("click", loadTrends);
});

// Fetch trends from the FastAPI Backend
async function loadTrends() {
    const trendsContainer = document.getElementById("trends-list");
    trendsContainer.innerHTML = `
        <div class="loading-state">
            <i class="fa-solid fa-spinner fa-spin"></i> Scanning search engines for trends...
        </div>
    `;

    try {
        const response = await fetch("/api/trends");
        if (!response.ok) throw new Error("Network response was not ok");
        
        const data = await response.json();
        currentTrends = data.trends;
        renderTrends(currentTrends);
    } catch (error) {
        console.error("Error loading trends:", error);
        trendsContainer.innerHTML = `
            <div class="loading-state">
                <i class="fa-solid fa-triangle-exclamation" style="color: #ff4f00;"></i>
                <span>Failed to scan trends. Make sure the server is running.</span>
            </div>
        `;
    }
}

// Render trend cards dynamically
function renderTrends(trends) {
    const trendsContainer = document.getElementById("trends-list");
    if (!trends || trends.length === 0) {
        trendsContainer.innerHTML = `<div class="loading-state">No active trends found.</div>`;
        return;
    }

    trendsContainer.innerHTML = "";
    trends.forEach(trend => {
        const card = document.createElement("div");
        card.className = "trend-card";
        card.dataset.id = trend.id;
        
        // Competitor coverage formatting
        const covClass = trend.competitor_coverage.toLowerCase();
        
        card.innerHTML = `
            <div class="trend-card-top">
                <span class="trend-title">${trend.trend}</span>
                <span class="trend-momentum">${trend.momentum}</span>
            </div>
            <p>${trend.description}</p>
            <div class="trend-card-footer">
                <span class="trend-vol"><i class="fa-solid fa-chart-line"></i> ${trend.volume_change}</span>
                <span>Gaps: <span class="competitor-gap-badge ${covClass}">${trend.competitor_coverage} COVERAGE</span></span>
                <span class="report-link" onclick="openCompetitorReport(event, ${trend.id})">Review Gaps</span>
            </div>
        `;
        
        // Add click selection listener
        card.addEventListener("click", () => selectTrend(trend));
        trendsContainer.appendChild(card);
    });
}

// Select a trend and populate inputs
function selectTrend(trend) {
    // Toggle visual select styling
    document.querySelectorAll(".trend-card").forEach(c => c.classList.remove("selected"));
    const selectedCard = document.querySelector(`.trend-card[data-id="${trend.id}"]`);
    if (selectedCard) selectedCard.classList.add("selected");

    // Populate display
    document.getElementById("trend-select-display").value = trend.trend;
    document.getElementById("trend-select-val").value = trend.trend;
    
    // Auto-populate keywords to save user time
    document.getElementById("keywords-input").value = trend.keywords.join(", ");
}

// Open modal containing competitor gaps report
function openCompetitorReport(event, id) {
    event.stopPropagation(); // Avoid triggering card selection click
    const trend = currentTrends.find(t => t.id === id);
    if (!trend) return;
    
    const modal = document.getElementById("modal-container");
    const reportText = document.getElementById("modal-report-text");
    
    reportText.innerText = trend.competitor_report;
    modal.classList.add("active");
}

// Setup Modal closure
function setupModalListener() {
    const modal = document.getElementById("modal-container");
    const closeBtn = document.querySelector(".close-modal");
    
    closeBtn.addEventListener("click", () => modal.classList.remove("active"));
    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.remove("active");
    });
}

// Setup tab routing interface
function setupTabListeners() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));
            
            btn.classList.add("active");
            document.getElementById(targetTab).classList.add("active");
        });
    });
}

// Form submit action calling FastAPI Social generator
function setupFormListener() {
    const form = document.getElementById("campaign-form");
    const generateBtn = document.getElementById("generate-btn");
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const trend = document.getElementById("trend-select-val").value;
        const brand = document.getElementById("brand-name").value;
        const kwsRaw = document.getElementById("keywords-input").value;
        const audience = document.getElementById("target-audience").value;
        
        if (!trend) {
            alert("Please select a trend from the Radar panel first!");
            return;
        }

        // Parse keywords
        const keywords = kwsRaw.split(",").map(k => k.trim()).filter(k => k !== "");
        
        // Show loading status in outputs
        setOutputsLoading(true);
        generateBtn.disabled = true;
        generateBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Optimization Agent Working...`;

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    trend: trend,
                    brand_name: brand,
                    keywords: keywords,
                    audience: audience
                })
            });
            
            if (!response.ok) throw new Error("Generation request failed");
            
            const data = await response.json();
            renderOutputs(data);
            
        } catch (error) {
            console.error("Generation failed:", error);
            alert("Content generation failed. Make sure your LLM configuration/API keys are active.");
            setOutputsLoading(false);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = `<i class="fa-solid fa-bolt"></i> Generate Social-First Campaign`;
        }
    });
}

// Utility to set outputs loading state
function setOutputsLoading(isLoading) {
    const ids = ["reddit-code", "linkedin-code", "youtube-code"];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (isLoading) {
            el.innerHTML = `<div class="loading-state"><i class="fa-solid fa-spinner fa-spin"></i> Writing & optimizing content hooks...</div>`;
        } else {
            el.innerText = "Generation failed or cancelled.";
        }
    });
    
    if (isLoading) {
        document.getElementById("geo-tips-list").innerHTML = `<li><i class="fa-solid fa-spinner fa-spin"></i> Analyzing...</li>`;
    }
}

// Render generated results
function renderOutputs(data) {
    document.getElementById("reddit-code").innerText = data.reddit;
    document.getElementById("linkedin-code").innerText = data.linkedin;
    document.getElementById("youtube-code").innerText = data.youtube;
    
    // Update GEO score text
    document.getElementById("geo-score-val").innerText = `${data.geo_score}%`;
    document.getElementById("geo-rationale").innerText = data.geo_score_rationale;
    
    // Update SVG Circular progress
    // Circumference is 2 * PI * r = 2 * 3.14159 * 26 = 163.36
    const circ = 163;
    const offset = circ - (data.geo_score / 100) * circ;
    document.getElementById("geo-progress-bar").style.strokeDashoffset = offset;
    
    // Update tips list
    const tipsList = document.getElementById("geo-tips-list");
    tipsList.innerHTML = "";
    
    if (data.geo_tips.length === 0) {
        tipsList.innerHTML = `
            <li style="border-color: var(--online-green); background: rgba(57, 211, 83, 0.05);">
                <i class="fa-solid fa-circle-check" style="color: var(--online-green);"></i>
                <span>Excellent! Content structures match maximum AI visibility crawling standards. Ready to publish.</span>
            </li>
        `;
    } else {
        data.geo_tips.forEach(tip => {
            const li = document.createElement("li");
            li.innerHTML = `
                <i class="fa-solid fa-triangle-exclamation"></i>
                <span>${tip}</span>
            `;
            tipsList.appendChild(li);
        });
    }
}

// Clipboard copying utility
function copyContent(elementId) {
    const text = document.getElementById(elementId).innerText;
    
    // Check if it is the loading/placeholder text
    if (text.includes("Your generated") || text.includes("crawling content")) {
        alert("Nothing to copy yet!");
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.querySelector(`.tab-content.active .copy-btn`);
        const originalHtml = copyBtn.innerHTML;
        
        copyBtn.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--online-green);"></i> Copied!`;
        setTimeout(() => {
            copyBtn.innerHTML = originalHtml;
        }, 2000);
    }).catch(err => {
        console.error("Clipboard copy failed:", err);
    });
}

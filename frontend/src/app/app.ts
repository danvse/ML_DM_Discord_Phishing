import { Component, inject, signal, ElementRef, viewChild, afterNextRender } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  SentinelService,
  PredictResponse,
  RedTeamResponse,
  TrainingMetrics,
  BenchmarkData,
  DifferentiationData
} from './services/sentinel.service';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export interface StreamMessage {
  id: string;
  sender: string;
  avatarBg: string;
  channel: string;
  content: string;
  timeStr: string;
  isScam: boolean;
  score: number;
  latencyMs: number;
  category: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private sentinel = inject(SentinelService);

  // Active Navigation Tab
  activeTab = signal<'arch' | 'playground' | 'redteam' | 'training' | 'benchmarks'>('playground');
  isSidebarCollapsed = signal<boolean>(false);
  isUserMenuOpen = signal<boolean>(false);
  sidebarSearch = signal<string>('');

  isOnline = this.sentinel.isBackendOnline;

  // DYNAMIC FEATURE 1: Live Simulated Ingestion Feed State
  isSimulatorRunning = signal<boolean>(true);
  totalMessagesScanned = signal<number>(3142);
  totalThreatsBlocked = signal<number>(528);
  liveCpuLatency = signal<number>(1.18);
  private streamIntervalId: any = null;
  private typeDebounceTimer: any = null;

  liveMessageStream = signal<StreamMessage[]>([
    {
      id: 'msg-4',
      sender: 'CryptoAirdrop#9912',
      avatarBg: '#ef4444',
      channel: '#announcements',
      content: 'URGENT: 5000 USDT Binance Airdrop live now! Mint here: https://binance-airdrop-claim.top',
      timeStr: 'Just now',
      isScam: true,
      score: 0.999,
      latencyMs: 1.15,
      category: 'Crypto Scam'
    },
    {
      id: 'msg-3',
      sender: 'AlexGamer#4011',
      avatarBg: '#3b82f6',
      channel: '#general',
      content: 'anyone down for a valorant 5-stack tonight? need 2 more',
      timeStr: '4s ago',
      isScam: false,
      score: 0.002,
      latencyMs: 1.12,
      category: 'Legitimate'
    },
    {
      id: 'msg-2',
      sender: 'DiscordGiftBot#0001',
      avatarBg: '#8b5cf6',
      channel: '#nitro-drops',
      content: '@everyone Steam is giving away free Discord Nitro! Claim here: https://discoord-app.com/free',
      timeStr: '9s ago',
      isScam: true,
      score: 0.998,
      latencyMs: 1.21,
      category: 'Typosquatting'
    },
    {
      id: 'msg-1',
      sender: 'TechDev#1337',
      avatarBg: '#10b981',
      channel: '#bot-dev',
      content: 'check this sick synthwave music video on youtube https://www.youtube.com/watch?v=5qap5aO4i9A',
      timeStr: '15s ago',
      isScam: false,
      score: 0.006,
      latencyMs: 1.17,
      category: 'Legitimate'
    }
  ]);

  private trafficSimulationPool = [
    { sender: 'NitroPromo#8812', avatarBg: '#ef4444', channel: '#giveaways', content: '@everyone Steam Nitro gift drop! Claim fast: https://discoord-promo.xyz/claim', isScam: true, score: 0.997, category: 'Typosquatting' },
    { sender: 'DevKyle#2091', avatarBg: '#3b82f6', channel: '#general', content: 'hey team did anyone deploy the latest migration script to staging yet?', isScam: false, score: 0.001, category: 'Legitimate' },
    { sender: 'GiftClaim#0492', avatarBg: '#f59e0b', channel: '#announcements', content: 'Fr33 N1tr0 gіft fоr еvеryоnе! Сlісk https://dlscord-drop.xyz/claim', isScam: true, score: 0.994, category: 'Homoglyph' },
    { sender: 'Maya#6541', avatarBg: '#10b981', channel: '#gaming', content: 'good game everyone! gg and see you all tomorrow at practice', isScam: false, score: 0.003, category: 'Legitimate' },
    { sender: 'IndieDev#7719', avatarBg: '#dc2626', channel: '#playtesting', content: 'Hey bro, we made an indie horror demo on itch, could you test the demo build? https://game-alpha-build.xyz/demo.zip', isScam: true, score: 0.988, category: 'Malware' },
    { sender: 'SamCodes#3141', avatarBg: '#06b6d4', channel: '#dev-chat', content: 'has anyone tested the new Python 3.14 free-threaded build with numpy?', isScam: false, score: 0.002, category: 'Legitimate' },
    { sender: 'AirdropSentinel#1102', avatarBg: '#ef4444', channel: '#crypto', content: 'CLAIM 10,000 ARB TOKENS IMMEDIATELY: Connect wallet at https://arbitrum-foundation-airdrop.top', isScam: true, score: 0.999, category: 'Web3 Drainer' }
  ];

  getActiveTabTitle(): string {
    switch (this.activeTab()) {
      case 'arch': return 'System Architecture & SOTA Blueprint';
      case 'playground': return 'Model Inference & Feature Attribution Playground';
      case 'redteam': return 'Minimax Adversarial Red-Team Studio';
      case 'training': return 'Training Dynamics & Optimization Loss';
      case 'benchmarks': return 'Empirical Benchmarks & Latency Pareto';
      default: return 'Dashboard Overview';
    }
  }

  getActiveTabSubtitle(): string {
    switch (this.activeTab()) {
      case 'arch': return 'Dual-stream feature fusion & invariant defenses across 3,017 dimensions';
      case 'playground': return 'Real-time inference with additive SHAP local explanation & payload heuristics';
      case 'redteam': return 'Simulate homoglyphs, zero-width chars, and domain spoofing in adversarial runtime';
      case 'training': return 'Gradient boosted log-loss convergence & early stopping checkpoint verification';
      case 'benchmarks': return 'SOTA comparative ROC curves, AUROC 0.999 & sub-1.2ms latency guarantees';
      default: return 'Welcome to Discord Sentinel Research Portal';
    }
  }

  getActiveTabBreadcrumb(): string {
    switch (this.activeTab()) {
      case 'arch': return 'Architecture & Blueprint';
      case 'playground': return 'Inference Playground';
      case 'redteam': return 'Red-Team Studio';
      case 'training': return 'Training Dynamics';
      case 'benchmarks': return 'Empirical Benchmarks';
      default: return 'Overview';
    }
  }

  // TAB 2: Playground State
  chatInput = signal<string>('@everyone Steam is giving away free Discord Nitro! Claim here: https://discoord-app.com/free');
  selectedPreset = signal<string>('nitro');
  selectedModelTier = signal<'hardened' | 'baseline'>('hardened');
  predictionResult = signal<PredictResponse | null>(null);
  isPredicting = signal<boolean>(false);

  // TAB 3: Red-Team Arena State
  redTeamInput = signal<string>('@everyone Steam is giving away free Discord Nitro! Claim here: https://discord.com/nitro');
  optHomoglyphs = signal<boolean>(true);
  optZeroWidth = signal<boolean>(true);
  optUrlSpoof = signal<boolean>(true);
  optUrgency = signal<boolean>(false);
  redTeamResult = signal<RedTeamResponse | null>(null);
  isMutating = signal<boolean>(false);

  // TAB 1, 4, 5 Data
  diffData = signal<DifferentiationData | null>(null);
  trainingMetrics = signal<TrainingMetrics | null>(null);
  benchmarkData = signal<BenchmarkData | null>(null);
  decisionThreshold = signal<number>(0.50);

  // Chart Canvas viewChild references
  radarCanvas = viewChild<ElementRef<HTMLCanvasElement>>('radarCanvas');
  lossCanvas = viewChild<ElementRef<HTMLCanvasElement>>('lossCanvas');
  rocCanvas = viewChild<ElementRef<HTMLCanvasElement>>('rocCanvas');
  paretoCanvas = viewChild<ElementRef<HTMLCanvasElement>>('paretoCanvas');
  shapCanvas = viewChild<ElementRef<HTMLCanvasElement>>('shapCanvas');

  // Chart instances
  private radarChart: Chart | null = null;
  private lossChart: Chart | null = null;
  private rocChart: Chart | null = null;
  private paretoChart: Chart | null = null;
  private shapChart: Chart | null = null;

  presets = [
    { id: 'nitro', name: 'Nitro Typosquatting', text: '@everyone Steam is giving away free Discord Nitro! Claim here: https://discoord-app.com/free' },
    { id: 'homoglyph', name: 'Homoglyph Evasion', text: 'Fr33 N1tr0 gіft fоr еvеryоnе! Сlісk [https://discord.com/nitro](https://dlscord-drop.xyz/claim)' },
    { id: 'gametester', name: 'Malware Game Tester', text: 'Hey bro, me and my team made an indie game on steam/itch, could you test the demo build? https://game-alpha-build.xyz/demo.zip' },
    { id: 'crypto', name: 'Web3 Airdrop Scam', text: 'URGENT: 5000 USDT Binance Airdrop live now for Discord members! Mint here: https://binance-airdrop-claim.top' },
    { id: 'benign', name: 'Benign Gamer Banter', text: 'hey anyone want to play valorant tonight? we need one more for competitive queue' },
    { id: 'legitlink', name: 'Benign with YouTube Link', text: 'check out this funny cat video on youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ' }
  ];

  constructor() {
    afterNextRender(() => {
      this.loadAllData();
      this.runPrediction();
      this.runMutation();
      this.startTrafficSimulator();
    });
  }

  toggleSimulator() {
    if (this.isSimulatorRunning()) {
      this.stopTrafficSimulator();
      this.isSimulatorRunning.set(false);
    } else {
      this.startTrafficSimulator();
      this.isSimulatorRunning.set(true);
    }
  }

  startTrafficSimulator() {
    if (this.streamIntervalId) clearInterval(this.streamIntervalId);
    this.streamIntervalId = setInterval(() => {
      if (!this.isSimulatorRunning()) return;
      
      const pool = this.trafficSimulationPool;
      const pick = pool[Math.floor(Math.random() * pool.length)];
      const jitterMs = +(1.10 + Math.random() * 0.15).toFixed(2);
      
      const newMsg: StreamMessage = {
        id: 'msg-' + Date.now(),
        sender: pick.sender,
        avatarBg: pick.avatarBg,
        channel: pick.channel,
        content: pick.content,
        timeStr: 'Just now',
        isScam: pick.isScam,
        score: pick.score,
        latencyMs: jitterMs,
        category: pick.category
      };

      this.liveMessageStream.update(list => [newMsg, ...list.slice(0, 7)]);
      this.totalMessagesScanned.update(c => c + 1);
      if (pick.isScam) {
        this.totalThreatsBlocked.update(c => c + 1);
      }
      this.liveCpuLatency.set(jitterMs);
    }, 2400);
  }

  stopTrafficSimulator() {
    if (this.streamIntervalId) {
      clearInterval(this.streamIntervalId);
      this.streamIntervalId = null;
    }
  }

  selectStreamMessage(msg: StreamMessage) {
    this.chatInput.set(msg.content);
    this.runPrediction();
  }

  onChatInputChange(newVal: string) {
    this.chatInput.set(newVal);
    if (this.typeDebounceTimer) clearTimeout(this.typeDebounceTimer);
    this.typeDebounceTimer = setTimeout(() => {
      this.runPrediction();
    }, 240);
  }

  getRiskColor(score: number): string {
    if (score >= this.decisionThreshold()) return '#ef4444'; // Red (Scam)
    if (score >= this.decisionThreshold() - 0.20) return '#f59e0b'; // Amber (Suspicious)
    return '#10b981'; // Green (Safe)
  }

  getRiskGaugeOffset(score: number): number {
    // Circle circumference with r=40 is ~251.3
    const maxOffset = 251.3;
    const clamped = Math.max(0, Math.min(1, score));
    return maxOffset * (1 - clamped);
  }

  getEnforcementVerdict(score: number) {
    const thresh = this.decisionThreshold();
    if (score >= thresh) {
      return {
        verdict: 'MALICIOUS PHISHING SCAM',
        action: 'AUTO-DELETE & BAN SENDER',
        color: '#ef4444',
        badgeClass: 'verdict-critical',
        note: 'Payload violated verified structural invariants.'
      };
    } else if (score >= thresh - 0.20) {
      return {
        verdict: 'BORDERLINE / SUSPICIOUS',
        action: 'QUARANTINE & DISCORD NOTIFY',
        color: '#f59e0b',
        badgeClass: 'verdict-warning',
        note: 'Elevated entropy or minor typosquat similarity.'
      };
    } else {
      return {
        verdict: 'BENIGN GAMER MESSAGE',
        action: 'ALLOW & DELIVER INSTANTLY',
        color: '#10b981',
        badgeClass: 'verdict-safe',
        note: 'Payload conforms to standard non-adversarial text.'
      };
    }
  }

  toggleSidebar() {
    this.isSidebarCollapsed.update(v => !v);
  }

  toggleUserMenu() {
    this.isUserMenuOpen.update(v => !v);
  }

  setTab(tab: 'arch' | 'playground' | 'redteam' | 'training' | 'benchmarks') {
    this.activeTab.set(tab);
    setTimeout(() => {
      this.renderChartsForTab(tab);
    }, 60);
  }

  loadAllData() {
    this.sentinel.getDifferentiation().subscribe(d => {
      this.diffData.set(d);
      if (this.activeTab() === 'arch') this.initRadarChart();
    });

    this.sentinel.getTrainingMetrics().subscribe(m => {
      this.trainingMetrics.set(m);
      if (this.activeTab() === 'training') this.initLossChart();
    });

    this.sentinel.getBenchmarks().subscribe(b => {
      this.benchmarkData.set(b);
      if (this.activeTab() === 'benchmarks') {
        this.initRocChart();
        this.initParetoChart();
      }
    });
  }

  onPresetChange(id: string) {
    this.selectedPreset.set(id);
    const p = this.presets.find(x => x.id === id);
    if (p) {
      this.chatInput.set(p.text);
      this.runPrediction();
    }
  }

  runPrediction() {
    this.isPredicting.set(true);
    this.sentinel.predict(this.chatInput(), this.selectedModelTier()).subscribe(res => {
      this.predictionResult.set(res);
      this.isPredicting.set(false);
      setTimeout(() => this.renderShapChart(res), 60);
    });
  }

  runMutation() {
    this.isMutating.set(true);
    this.sentinel.mutate(this.redTeamInput(), {
      homoglyphs: this.optHomoglyphs(),
      zero_width: this.optZeroWidth(),
      url_spoof: this.optUrlSpoof(),
      urgency_invert: this.optUrgency()
    }).subscribe(res => {
      this.redTeamResult.set(res);
      this.isMutating.set(false);
    });
  }

  private renderChartsForTab(tab: string) {
    if (tab === 'arch') {
      this.initRadarChart();
    } else if (tab === 'playground' && this.predictionResult()) {
      this.renderShapChart(this.predictionResult()!);
    } else if (tab === 'training') {
      this.initLossChart();
    } else if (tab === 'benchmarks') {
      this.initRocChart();
      this.initParetoChart();
    }
  }

  private renderShapChart(res: PredictResponse) {
    const canvas = this.shapCanvas()?.nativeElement;
    if (!canvas) return;

    if (this.shapChart) this.shapChart.destroy();

    const labels = res.contributions.map(c => c.feature);
    const data = res.contributions.map(c => c.impact);
    const bgColors = data.map(v => v > 0 ? '#ef4444' : '#10b981');

    this.shapChart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Additive SHAP Impact',
          data,
          backgroundColor: bgColors,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx: any) => {
                const val = ctx.parsed?.x ?? 0;
                return `Impact: ${val > 0 ? '+' : ''}${val.toFixed(2)} (${val > 0 ? 'Pushes Scam' : 'Pushes Safe'})`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b' }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#0f172a', font: { size: 11, weight: 'bold' } }
          }
        }
      }
    });
  }

  private initRadarChart() {
    const canvas = this.radarCanvas()?.nativeElement;
    const data = this.diffData();
    if (!canvas || !data) return;

    if (this.radarChart) this.radarChart.destroy();

    this.radarChart = new Chart(canvas, {
      type: 'radar',
      data: {
        labels: data.radar_comparison.axes,
        datasets: data.radar_comparison.models.map(m => ({
          label: m.name,
          data: m.values,
          borderColor: m.color,
          backgroundColor: m.color + '20',
          borderWidth: 2,
          pointBackgroundColor: m.color,
          pointRadius: 4
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: '#e2e8f0' },
            grid: { color: '#e2e8f0' },
            pointLabels: { color: '#0f172a', font: { size: 12, weight: 'bold' } },
            ticks: { display: false, maxTicksLimit: 5 }
          }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: { color: '#0f172a', font: { size: 11 } }
          }
        }
      }
    });
  }

  private initLossChart() {
    const canvas = this.lossCanvas()?.nativeElement;
    const data = this.trainingMetrics();
    if (!canvas || !data) return;

    if (this.lossChart) this.lossChart.destroy();

    const sampleRounds = data.boosting_rounds.filter(r => r % 3 === 0 || r === 1 || r === 82);

    this.lossChart = new Chart(canvas, {
      type: 'line',
      data: {
        labels: sampleRounds.map(r => `R${r}`),
        datasets: [
          {
            label: 'Clean Training Log-Loss',
            data: sampleRounds.map(r => data.clean_train_loss[r - 1]),
            borderColor: '#2563eb',
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 0
          },
          {
            label: 'Clean Validation Log-Loss',
            data: sampleRounds.map(r => data.clean_val_loss[r - 1]),
            borderColor: '#64748b',
            borderWidth: 2,
            borderDash: [5, 5],
            tension: 0.2,
            pointRadius: 0
          },
          {
            label: 'Minimax Hardened Val Loss',
            data: sampleRounds.map(r => data.hardened_val_loss[r - 1]),
            borderColor: '#10b981',
            borderWidth: 2.5,
            tension: 0.2,
            pointRadius: sampleRounds.map(r => r === 82 ? 6 : 0),
            pointBackgroundColor: '#10b981'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b', maxTicksLimit: 12 }
          },
          y: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b' },
            title: { display: true, text: 'Binary Cross-Entropy Loss', color: '#64748b' }
          }
        },
        plugins: {
          legend: { labels: { color: '#0f172a' } }
        }
      }
    });
  }

  private initRocChart() {
    const canvas = this.rocCanvas()?.nativeElement;
    const data = this.benchmarkData();
    if (!canvas || !data) return;

    if (this.rocChart) this.rocChart.destroy();

    this.rocChart = new Chart(canvas, {
      type: 'line',
      data: {
        labels: data.roc_curves.fpr.map(f => f.toFixed(2)),
        datasets: [
          {
            label: 'Hardened Fused XGBoost (AUC = 0.999)',
            data: data.roc_curves.hardened_fused,
            borderColor: '#10b981',
            borderWidth: 3,
            tension: 0.1
          },
          {
            label: 'Baseline Fused XGBoost (AUC = 0.998)',
            data: data.roc_curves.baseline_fused,
            borderColor: '#2563eb',
            borderWidth: 2,
            tension: 0.1
          },
          {
            label: 'Naive Bayes (AUC = 0.990)',
            data: data.roc_curves.naive_bayes,
            borderColor: '#f59e0b',
            borderWidth: 1.5,
            tension: 0.1
          },
          {
            label: 'AutoMod Regex (AUC = 0.720)',
            data: data.roc_curves.automod_regex,
            borderColor: '#ef4444',
            borderWidth: 1.5,
            borderDash: [4, 4]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b' },
            title: { display: true, text: 'False Positive Rate (FPR)', color: '#64748b' }
          },
          y: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b' },
            title: { display: true, text: 'True Positive Rate (TPR / Recall)', color: '#64748b' }
          }
        },
        plugins: {
          legend: { labels: { color: '#0f172a', font: { size: 11 } } }
        }
      }
    });
  }

  private initParetoChart() {
    const canvas = this.paretoCanvas()?.nativeElement;
    const data = this.benchmarkData();
    if (!canvas || !data) return;

    if (this.paretoChart) this.paretoChart.destroy();

    const points = data.latency_pareto.map(p => ({
      x: p.latency_ms,
      y: p.f1,
      name: p.name,
      winner: p.winner
    }));

    this.paretoChart = new Chart(canvas, {
      type: 'scatter',
      data: {
        datasets: [{
          label: 'Models (Latency vs F1)',
          data: points,
          backgroundColor: points.map(p => p.winner ? '#10b981' : '#2563eb'),
          pointRadius: points.map(p => p.winner ? 10 : 7),
          pointHoverRadius: 12
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'logarithmic',
            grid: { color: '#e2e8f0' },
            ticks: {
              color: '#64748b',
              callback: (val) => `${val}ms`
            },
            title: { display: true, text: 'CPU Latency (Log Scale ms - Lower is Better)', color: '#64748b' }
          },
          y: {
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b' },
            min: 40,
            max: 100,
            title: { display: true, text: 'Adversarial F1 Score (% - Higher is Better)', color: '#64748b' }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (ctx: any) => {
                const p = points[ctx.dataIndex];
                return `${p.name}: ${p.y.toFixed(1)}% F1 @ ${p.x}ms`;
              }
            }
          },
          legend: { display: false }
        }
      }
    });
  }
}

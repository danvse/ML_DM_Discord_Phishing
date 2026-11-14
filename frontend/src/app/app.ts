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

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private sentinel = inject(SentinelService);

  // Active Tab
  activeTab = signal<'arch' | 'playground' | 'redteam' | 'training' | 'benchmarks'>('arch');

  isOnline = this.sentinel.isBackendOnline;

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
    });
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
    const bgColors = data.map(v => v > 0 ? '#dc2626' : '#059669');

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
            borderColor: '#059669',
            borderWidth: 2.5,
            tension: 0.2,
            pointRadius: sampleRounds.map(r => r === 82 ? 6 : 0),
            pointBackgroundColor: '#059669'
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
            borderColor: '#059669',
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
            borderColor: '#dc2626',
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
          backgroundColor: points.map(p => p.winner ? '#059669' : '#2563eb'),
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

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { Boxes, GitBranch, AlertTriangle, Search, TrendingUp, TrendingDown, Network } from "lucide-react";
import { getDashboard, type DashboardData } from "../api";
import { ICONS } from "../lib/ui";

function Kpi({ label, value, icon: Icon, tone }: { label: string; value: number; icon: any; tone: string }) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-500">{label}</span>
        <span className={`flex h-9 w-9 items-center justify-center rounded-xl ${tone}`}>
          <Icon className="h-5 w-5" />
        </span>
      </div>
      <div className="mt-3 text-3xl font-bold tabular-nums text-slate-900">{value.toLocaleString()}</div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    getDashboard().then(setData).catch((e) => setErr(String(e)));
  }, []);

  if (err) return <div className="card p-6 text-rose-600">대시보드 로드 실패: {err}</div>;
  if (!data) return <div className="text-slate-400">불러오는 중…</div>;

  const barData = [...data.category].sort((a, b) => b.count - a.count);
  const colors = ["#3a5eef", "#5b84fa", "#8fb0ff"];

  return (
    <div className="space-y-8">
      <header className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">ITSM 통합관리 대시보드</h1>
          <p className="mt-1 text-sm text-slate-500">구성·변경·장애·문제 현황을 한눈에 관제합니다.</p>
        </div>
        <span className="chip bg-emerald-100 text-emerald-700">● 실시간 CSV 연동</span>
      </header>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Kpi label="총 자산 수" value={data.kpis.totalAssets} icon={Boxes} tone="bg-brand-100 text-brand-600" />
        <Kpi label="변경 건수" value={data.kpis.change} icon={GitBranch} tone="bg-indigo-100 text-indigo-600" />
        <Kpi label="장애 건수" value={data.kpis.incident} icon={AlertTriangle} tone="bg-rose-100 text-rose-600" />
        <Kpi label="문제 건수" value={data.kpis.problem} icon={Search} tone="bg-amber-100 text-amber-600" />
      </section>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="card p-6 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold text-slate-900">카테고리별 자산 현황</h2>
            <span className="text-xs text-slate-400">3_구성관리 / CI.csv</span>
          </div>
          <ResponsiveContainer width="100%" height={360}>
            <BarChart data={barData} layout="vertical" margin={{ left: 24, right: 24 }}>
              <CartesianGrid horizontal={false} stroke="#eef1f6" />
              <XAxis type="number" tick={{ fontSize: 12, fill: "#98a2b3" }} axisLine={false} tickLine={false} />
              <YAxis
                type="category" dataKey="label" width={110}
                tick={{ fontSize: 12, fill: "#475467" }} axisLine={false} tickLine={false}
              />
              <Tooltip
                cursor={{ fill: "#f4f6fb" }}
                formatter={(v) => [`${v}건`, "자산수"]}
                contentStyle={{ borderRadius: 12, border: "1px solid #e5e9f2", fontSize: 12 }}
              />
              <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={16}>
                {barData.map((_, i) => (
                  <Cell key={i} fill={colors[i % colors.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-4">
          <div className="card p-5">
            <h2 className="mb-3 font-semibold text-slate-900">구성 이력</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between rounded-xl bg-emerald-50 px-4 py-3">
                <span className="flex items-center gap-2 text-sm text-emerald-700">
                  <TrendingUp className="h-4 w-4" /> 자산 추가
                </span>
                <span className="text-lg font-bold text-emerald-700">{data.kpis.ciAdded}</span>
              </div>
              <div className="flex items-center justify-between rounded-xl bg-rose-50 px-4 py-3">
                <span className="flex items-center gap-2 text-sm text-rose-700">
                  <TrendingDown className="h-4 w-4" /> 자산 삭제
                </span>
                <span className="text-lg font-bold text-rose-700">{data.kpis.ciRemoved}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="mb-3 font-semibold text-slate-900">운영 도메인 바로가기</h2>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          {data.domainCounts.map((d) => {
            const Icon = ICONS[d.icon] ?? Network;
            return (
              <Link key={d.key} to={`/d/${d.key}`} className="card group p-4 transition hover:shadow-pop">
                <div className="flex items-center gap-2 text-slate-500 group-hover:text-brand-600">
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{d.title}</span>
                </div>
                <div className="mt-2 text-2xl font-bold tabular-nums text-slate-900">{d.count}</div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
}

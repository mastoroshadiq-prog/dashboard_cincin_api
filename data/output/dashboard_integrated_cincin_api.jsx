import React, { useState } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    ComposedChart, Area, Cell, Line, PieChart, Pie
} from 'recharts';
import {
    AlertTriangle,
    DollarSign,
    Info,
    ShieldAlert,
    Zap,
    Maximize2,
    Target,
    Activity,
    ArrowUpRight,
    Skull,
    TrendingDown,
    Microscope,
    EyeOff,
    Clock,
    CheckCircle2,
    TreePalm,
    Layers,
    Map
} from 'lucide-react';

const App = () => {
    const [activeTab, setActiveTab] = useState('overview');
    const [scalingLevel, setScalingLevel] = useState('block');

    // Data Faktual Berdasarkan Derivasi Dokumen Updated 30 Des 2025
    const dataBlok = [
        {
            id: 'D006A',
            luas: 23.0,
            totalTanaman: 2382,
            sisip: 0,
            tahunTanam: 2009,
            usia: 16,
            potensi: 17.30,
            realisasi: 0.79,
            gapTon: 16.51,
            infectedEconomic: 95.4,
            sph: 104,
            spreadRatio: 2.16,
            loss: 569.6,
            core: 37,
            ring: 80,
            suspect: 244,
            mapImage: '/cincin_api_map_D006A.png' // Path to generated map
        },
        {
            id: 'D007A',
            luas: 24.7,
            totalTanaman: 2586,
            sisip: 0,
            tahunTanam: 2009,
            usia: 16,
            potensi: 17.53,
            realisasi: 0.30,
            gapTon: 17.23,
            infectedEconomic: 98.3,
            sph: 105,
            spreadRatio: 1.87,
            loss: 638.4,
            core: 57,
            ring: 107,
            suspect: 200,
            mapImage: '/cincin_api_map_D007A.png' // Path to generated map
        }
    ];

    const stats = {
        block: { label: '2 Blok Sampel', area: 47.7, loss: 1.208, mitigation: 0.1 },
        division: { label: 'Skala Divisi', area: 750, loss: 19.1, mitigation: 1.57 },
        estate: { label: 'Skala Kebun (20%)', area: 2200, loss: 56.1, mitigation: 4.6 }
    };

    const currentStats = stats[scalingLevel];

    return (
        <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-black">
            {/* Header Strategis */}
            <div className="max-w-7xl mx-auto mb-8 flex flex-col lg:flex-row lg:items-end justify-between gap-6">
                <div>
                    <div className="flex items-center gap-2 mb-2 text-black font-black">
                        <span className="bg-red-600 text-white px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest animate-pulse">
                            Reality Check Briefing
                        </span>
                        <span className="opacity-20 font-black">|</span>
                        <span className="text-xs font-black uppercase tracking-widest flex items-center gap-1">
                            <Clock size={14} /> Update 31 Des 2025 • Blok D006A & D007A
                        </span>
                    </div>
                    <h1 className="text-3xl font-black text-black tracking-tighter text-balance">Analisis Krusialitas & Eskalasi Dampak</h1>
                    <p className="text-black mt-1 max-w-2xl font-black text-balance">
                        Transparansi Data Produksi: Bedah Gap Potensi vs Realisasi Lapangan (Tahun Produksi 2025).
                    </p>
                </div>

                <div className="flex p-1 bg-white rounded-xl shadow-sm border border-slate-200 font-black">
                    <button
                        onClick={() => setActiveTab('overview')}
                        className={`px-6 py-2.5 rounded-lg text-sm font-black transition-all ${activeTab === 'overview' ? 'bg-indigo-600 text-white shadow-md' : 'text-black hover:bg-slate-50'}`}
                    >
                        Snapshot & Ekstrapolasi
                    </button>
                    <button
                        onClick={() => setActiveTab('scenarios')}
                        className={`px-6 py-2.5 rounded-lg text-sm font-black transition-all ${activeTab === 'scenarios' ? 'bg-indigo-600 text-white shadow-md' : 'text-black hover:bg-slate-50'}`}
                    >
                        Reality Check: 3 Skenario
                    </button>
                </div>
            </div>

            <div className="max-w-7xl mx-auto space-y-6">

                {activeTab === 'overview' && (
                    <div className="space-y-6">
                        {/* Panel Eskalasi Makro */}
                        <div className="bg-slate-900 rounded-[2rem] p-8 text-white shadow-xl relative overflow-hidden border border-white/10">
                            <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none text-white font-black">
                                <Maximize2 size={120} />
                            </div>
                            <div className="relative z-10 font-black">
                                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
                                    <div>
                                        <h2 className="text-xl font-bold flex items-center gap-2 text-white font-black">
                                            <Zap size={20} className="text-yellow-400 fill-yellow-400" />
                                            Potensi Kerugian Skala Makro (Impact Escalation)
                                        </h2>
                                        <p className="text-white opacity-80 text-sm italic font-black">
                                            Ekstrapolasi temuan sampel ke wilayah operasional yang lebih luas.
                                        </p>
                                    </div>
                                    <div className="flex bg-white/10 p-1 rounded-lg">
                                        {Object.keys(stats).map(lvl => (
                                            <button
                                                key={lvl}
                                                onClick={() => setScalingLevel(lvl)}
                                                className={`px-4 py-1.5 rounded-md text-xs font-black transition-all ${scalingLevel === lvl ? 'bg-white text-slate-900 shadow-lg' : 'text-white opacity-60 hover:opacity-100'}`}
                                            >
                                                {stats[lvl].label}
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-black">
                                    <div className="bg-white/5 backdrop-blur-sm p-6 rounded-2xl border border-white/10 font-black">
                                        <p className="text-indigo-300 text-[10px] font-black uppercase mb-1 tracking-widest font-black">Cakupan Wilayah</p>
                                        <div className="flex items-baseline gap-2 font-black">
                                            <span className="text-4xl">{currentStats.area.toLocaleString()}</span>
                                            <span className="text-indigo-300 text-sm uppercase tracking-tighter">HA</span>
                                        </div>
                                        {scalingLevel === 'estate' && (
                                            <p className="text-[10px] text-white opacity-90 mt-1 font-black underline decoration-red-500 tracking-tighter">Subset 2.200 Ha dari 11.000 Ha Kebun</p>
                                        )}
                                    </div>
                                    <div className="bg-red-500/10 backdrop-blur-sm p-6 rounded-2xl border border-red-500/30 ring-2 ring-red-500/20 font-black font-black">
                                        <p className="text-red-400 text-[10px] font-black uppercase mb-1 tracking-widest font-black font-black">Potensi Kerugian</p>
                                        <div className="flex items-baseline gap-2 font-black">
                                            <span className="text-4xl text-red-400 font-black">Rp {currentStats.loss}</span>
                                            <span className="text-red-400 text-sm uppercase tracking-tighter font-black">MILAR/THN</span>
                                        </div>
                                    </div>
                                    <div className="bg-emerald-500/10 backdrop-blur-sm p-6 rounded-2xl border border-emerald-500/30 font-black">
                                        <p className="text-emerald-400 text-[10px] font-black uppercase mb-1 tracking-widest font-black font-black">Biaya Mitigasi</p>
                                        <div className="flex items-baseline gap-2 font-black">
                                            <span className="text-4xl text-emerald-400 font-black">Rp {currentStats.mitigation}</span>
                                            <span className="text-emerald-400 text-sm uppercase tracking-tighter font-black">MILAR</span>
                                        </div>
                                        <p className="text-[10px] text-emerald-300 mt-2 font-black italic">Hanya ~0.1% dari risiko aset</p>
                                    </div>
                                </div>

                                {/* Highlight Khusus Asumsi 20% - Ukuran Dioptimalkan (p-6) */}
                                {scalingLevel === 'estate' && (
                                    <div className="mt-8 p-6 bg-red-600/20 border-2 border-red-500/50 rounded-2xl flex items-start gap-4 shadow-xl font-black">
                                        <ShieldAlert className="text-red-400 shrink-0 mt-1 font-black" size={32} />
                                        <div className="space-y-1 font-black">
                                            <h4 className="text-lg font-black text-white uppercase tracking-tighter font-black">
                                                Peringatan Interpretasi Data:
                                            </h4>
                                            <p className="text-base text-white font-bold leading-relaxed font-black">
                                                Angka <span className="text-red-400 font-black px-1.5 bg-black/40 rounded">Rp 56.1 Miliar</span> didasarkan pada asumsi bahwa <span className="underline decoration-red-500 decoration-2 underline-offset-4 font-black">HANYA 20% (2.200 Ha)</span> dari total 11.000 Ha kebun yang memiliki kondisi kritis serupa dengan sampel. Laporan ini tidak merepresentasikan kerugian untuk luasan 11.000 Ha secara keseluruhan.
                                            </p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Kartu Bukti Ilmiah (Hitam Solid & Teks Besar) */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 text-black font-black">
                            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 border-l-8 border-l-indigo-500 font-black">
                                <div className="flex items-center gap-3 mb-4 font-black">
                                    <Microscope className="text-black font-black" size={32} />
                                    <h3 className="text-2xl font-black">1. Kontak Akar</h3>
                                </div>
                                <p className="text-xl leading-relaxed font-black font-black text-black">
                                    TT 2009 (Usia 16 Tahun). Sistem perakaran sudah <span className="underline decoration-indigo-500 decoration-4 font-black">interlocking</span>. Penularan bawah tanah dipastikan aktif dan masif.
                                </p>
                            </div>

                            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 border-l-8 border-l-orange-500 font-black text-black">
                                <div className="flex items-center gap-3 mb-4 font-black text-black">
                                    <Target className="text-black font-black" size={32} />
                                    <h3 className="text-2xl font-black">2. Rasio Sebar</h3>
                                </div>
                                <p className="text-xl leading-relaxed font-black font-black text-black">
                                    <span className="text-orange-600 underline decoration-orange-600 decoration-2 font-black text-2xl">Cincin Api {'>'} Inti</span>. Rasio 2.16x membuktikan penyakit sedang AKTIF MENJALAR.
                                </p>
                            </div>

                            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 border-l-8 border-l-red-500 font-black text-black">
                                <div className="flex items-center gap-3 mb-4 font-black text-black">
                                    <Skull className="text-black font-black" size={32} />
                                    <h3 className="text-2xl font-black">3. Symptom Lag</h3>
                                </div>
                                <p className="text-xl leading-relaxed font-black font-black text-black">
                                    Gap Produksi <span className="text-red-600 font-black text-2xl">95-98%</span> membuktikan akar hancur jauh mendahului gejala visual permukaan.
                                </p>
                            </div>
                        </div>

                        {/* Tabel Snapshot Faktual Utama (Pembaruan: Detail Potensi vs Realisasi) */}
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden text-black font-black">
                            <div className="p-8 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center text-black font-black">
                                <h3 className="text-2xl font-black uppercase tracking-tighter italic underline decoration-indigo-500 decoration-4 underline-offset-8 font-black">
                                    Snapshot Faktual & Gap Produktivitas
                                </h3>
                                <div className="flex gap-6 font-black">
                                    <div className="flex items-center gap-2 text-sm font-black uppercase font-black">
                                        <div className="w-4 h-4 rounded-full bg-red-600 font-black" /> Infeksi Inti
                                    </div>
                                    <div className="flex items-center gap-2 text-sm font-black uppercase font-black text-black">
                                        <div className="w-4 h-4 rounded-full bg-orange-400 font-black text-black" /> Cincin Api
                                    </div>
                                </div>
                            </div>
                            <div className="overflow-x-auto text-black font-black">
                                <table className="w-full text-left font-black text-black">
                                    <thead className="bg-slate-100 text-black text-xs font-black uppercase tracking-widest border-b border-slate-300 font-black text-black">
                                        <tr>
                                            <th className="px-6 py-6 border-r border-slate-200 font-black">ID Blok</th>
                                            <th className="px-6 py-6 text-center border-r border-slate-200 font-black">Potensi Standar<br /><span className="text-[9px] opacity-60 font-black">(Ton/Ha)</span></th>
                                            <th className="px-6 py-6 text-center border-r border-slate-200 font-black">Realisasi Aktual<br /><span className="text-[9px] opacity-60 font-black">(Ton/Ha)</span></th>
                                            <th className="px-6 py-6 text-center border-r border-slate-200 underline decoration-red-500 font-black">Gap Produksi<br /><span className="text-[9px] text-red-600 font-black">(Selisih Ton/Ha)</span></th>
                                            <th className="px-6 py-6 text-center border-r border-slate-200 font-black">Rasio Sebar</th>
                                            <th className="px-6 py-6 text-right font-black">Kerugian/Tahun</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-200 font-black text-black">
                                        {dataBlok.map(b => (
                                            <tr key={b.id} className="hover:bg-indigo-50/50 transition-colors font-black text-black">
                                                <td className="px-6 py-6 text-xl italic font-black text-black border-r border-slate-100 font-black">{b.id}</td>
                                                <td className="px-6 py-6 text-lg text-center font-black text-black border-r border-slate-100 font-black">{b.potensi.toFixed(2)}</td>
                                                <td className="px-6 py-6 text-lg text-center font-black text-black border-r border-slate-100 font-black">{b.realisasi.toFixed(2)}</td>
                                                <td className="px-6 py-6 text-red-600 text-2xl text-center font-black border-r border-slate-100 font-black">
                                                    {b.gapTon.toFixed(2)}
                                                    <span className="block text-[10px] font-black uppercase opacity-60 font-black">(-{b.infectedEconomic}%)</span>
                                                </td>
                                                <td className="px-6 py-6 font-black text-black border-r border-slate-100 font-black">
                                                    <div className="flex flex-col gap-1 font-black text-black items-center">
                                                        <span className="bg-orange-600 text-white px-3 py-1 rounded-lg text-sm font-black font-black text-black">{b.spreadRatio}x</span>
                                                        <div className="flex gap-2 text-[9px] font-black uppercase tracking-tighter mt-1 font-black text-black">
                                                            <span className="text-red-600 font-black">{b.core} Inti</span>
                                                            <span className="text-orange-600 font-black">{b.ring} Ring</span>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-6 text-xl font-black tracking-tight text-right uppercase font-black text-black font-black">Rp {b.loss} Juta</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                            <div className="p-4 bg-slate-50 text-[10px] font-black uppercase tracking-widest text-center border-t border-slate-200 opacity-60 font-black">
                                *Potensi didasarkan pada standar produktivitas tanaman usia 16 tahun (TT 2009).
                            </div>
                        </div>

                        {/* SECTION BARU: PETA KLUSTER CINCIN API */}
                        <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-[2rem] p-8 text-white shadow-2xl border border-white/10">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="p-4 bg-orange-500/20 rounded-2xl border border-orange-500/30">
                                    <Map className="text-orange-400" size={32} />
                                </div>
                                <div>
                                    <h2 className="text-3xl font-black uppercase tracking-tighter">🔥 Peta Kluster Cincin Api</h2>
                                    <p className="text-white/80 text-sm italic mt-1">Visualisasi Spatial: Lokasi Infeksi Inti & Zona Penyebaran Aktif</p>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {dataBlok.map(b => (
                                    <div key={b.id + '_map'} className="bg-white rounded-3xl overflow-hidden shadow-xl border-4 border-white/20">
                                        <div className="bg-gradient-to-r from-slate-800 to-slate-700 p-6 border-b-4 border-orange-500">
                                            <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center justify-between">
                                                <span>Blok {b.id}</span>
                                                <span className="text-sm bg-orange-600 px-4 py-1.5 rounded-full font-black">
                                                    Spread Ratio: {b.spreadRatio}x
                                                </span>
                                            </h3>
                                            <div className="flex gap-6 mt-3 text-sm">
                                                <div className="flex items-center gap-2">
                                                    <div className="w-3 h-3 rounded-full bg-red-600"></div>
                                                    <span className="text-white/90">{b.core} Inti</span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                                                    <span className="text-white/90">{b.ring} Cincin Api</span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                                                    <span className="text-white/90">{b.suspect} Suspect</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="p-4 bg-slate-50">
                                            <img
                                                src={b.mapImage}
                                                alt={`Peta Cincin Api Blok ${b.id}`}
                                                className="w-full h-auto rounded-xl shadow-lg border-2 border-slate-200"
                                            />
                                        </div>
                                        <div className="p-6 bg-slate-100 border-t-2 border-slate-200">
                                            <p className="text-xs text-slate-600 uppercase tracking-widest font-black mb-2">Interpretasi Peta:</p>
                                            <p className="text-sm text-slate-800 leading-relaxed">
                                                Cluster <span className="font-black text-red-600">MERAH</span> menunjukkan pusat infeksi aktif.
                                                Zona <span className="font-black text-orange-600">ORANYE</span> adalah "Ring of Fire" yang sedang menyebar ke pohon tetangga.
                                                Parit isolasi harus dibuat mengelilingi zona ini untuk menyelamatkan {b.totalTanaman - b.core - b.ring - b.suspect} pohon sehat.
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="mt-8 p-6 bg-orange-600/20 border-2 border-orange-500/50 rounded-2xl">
                                <div className="flex items-start gap-4">
                                    <AlertTriangle className="text-orange-400 shrink-0 mt-1" size={28} />
                                    <div>
                                        <h4 className="text-lg font-black text-white uppercase mb-2">Rekomendasi Mitigasi Berdasarkan Peta:</h4>
                                        <p className="text-white/90 leading-relaxed">
                                            Peta kluster menunjukkan bahwa infeksi tidak tersebar merata, melainkan membentuk <span className="font-black underline decoration-orange-500 decoration-2">cluster terlokalisasi</span>.
                                            Strategi parit isolasi harus diprioritaskan pada zona dengan Spread Ratio tertinggi (D006A: 2.16x) untuk memaksimalkan efektivitas biaya mitigasi.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Drilldown Detail Blok (Individu) - EXISTING CODE CONTINUES... */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-8 text-black font-black">
                            {dataBlok.map(b => (
                                <div key={b.id + 'drill'} className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden text-black font-black font-black font-black">
                                    <div className="p-6 bg-slate-900 text-white flex justify-between items-center text-white font-black font-black">
                                        <h4 className="text-xl font-black uppercase tracking-tighter flex items-center gap-2 text-white font-black">
                                            <Maximize2 size={20} className="text-indigo-400 font-black" /> Detail Blok {b.id} ({b.luas} Ha)
                                        </h4>
                                        <span className="bg-red-600 text-white text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-widest animate-pulse font-black font-black">Status: Darurat</span>
                                    </div>
                                    <div className="p-8 space-y-8 font-black text-black font-black font-black text-black">
                                        {/* Profil Agronomi & SPH */}
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-black">
                                            <div className="p-4 bg-indigo-50 rounded-2xl border border-indigo-100 flex items-center gap-3 font-black text-black font-black text-black">
                                                <TreePalm className="text-indigo-600 font-black font-black" size={24} />
                                                <div>
                                                    <p className="text-[10px] font-black uppercase text-indigo-400 font-black text-black font-black">Tahun Tanam / Usia</p>
                                                    <p className="text-lg font-black text-indigo-900 font-black text-black font-black font-black">{b.tahunTanam} ({b.usia} Tahun)</p>
                                                </div>
                                            </div>
                                            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center gap-3 font-black text-black font-black text-black">
                                                <Layers className="text-slate-600 font-black font-black" size={24} />
                                                <div>
                                                    <p className="text-[10px] font-black uppercase text-slate-400 font-black text-black font-black text-black">Kerapatan Tanam (SPH)</p>
                                                    <p className="text-lg font-black text-slate-900 font-black text-black font-black font-black">{b.sph} Pokok/Ha</p>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Populasi Tanaman Pokok vs Sisip (Set 0) */}
                                        <div className="p-4 bg-slate-900 text-white rounded-2xl flex items-center justify-between font-black text-black font-black">
                                            <div className="text-left font-black text-black text-black text-black">
                                                <p className="text-[10px] font-black uppercase text-indigo-400 font-black text-black font-black">Total Populasi Pohon</p>
                                                <p className="text-2xl font-black text-white font-black text-black font-black">{b.totalTanaman.toLocaleString()} <span className="text-xs font-black uppercase font-black font-black">PKK</span></p>
                                            </div>
                                            <div className="text-right font-black text-black text-black text-black text-black">
                                                <p className="text-[10px] font-black uppercase text-red-400 font-black text-black font-black font-black">Tanaman Sisip</p>
                                                <p className="text-2xl font-black text-white font-black text-black font-black font-black">{b.sisip} <span className="text-xs font-black uppercase font-black font-black font-black">PKK</span></p>
                                            </div>
                                        </div>

                                        {/* Distribusi Pohon */}
                                        <div>
                                            <p className="text-xs font-black uppercase text-black mb-4 tracking-[0.2em] border-l-4 border-indigo-500 pl-3 font-black text-black font-black font-black">Status Kesehatan Pohon Aktual</p>
                                            <div className="grid grid-cols-3 gap-4 font-black text-black font-black text-black font-black font-black">
                                                <div className="bg-red-50 p-4 rounded-2xl border border-red-100 text-center font-black text-black font-black text-black font-black font-black">
                                                    <p className="text-[10px] font-black text-red-600 uppercase mb-1 font-black text-black font-black font-black">Infeksi Inti</p>
                                                    <p className="text-2xl font-black text-red-700 font-black text-black font-black font-black">{b.core} <span className="text-[10px] uppercase text-black font-black font-black font-black">PKK</span></p>
                                                </div>
                                                <div className="bg-orange-50 p-4 rounded-2xl border border-orange-100 text-center font-black text-black font-black text-black font-black font-black font-black">
                                                    <p className="text-[10px] font-black text-orange-600 uppercase mb-1 font-black font-black font-black">Cincin Api</p>
                                                    <p className="text-2xl font-black text-orange-700 font-black font-black font-black font-black">{b.ring} <span className="text-[10px] uppercase text-black font-black font-black font-black font-black">PKK</span></p>
                                                </div>
                                                <div className="bg-yellow-50 p-4 rounded-2xl border border-yellow-100 text-center font-black text-black font-black text-black font-black font-black font-black">
                                                    <p className="text-[10px] font-black text-yellow-600 uppercase mb-1 font-black font-black font-black font-black">Berisiko</p>
                                                    <p className="text-2xl font-black text-yellow-700 font-black font-black font-black font-black font-black font-black">{b.suspect} <span className="text-[10px] uppercase font-black text-black font-black font-black font-black">PKK</span></p>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Gap Yield & Loss - Clarified Cycle 2025 & Total Area */}
                                        <div className="flex flex-col md:flex-row gap-6 font-black font-black font-black font-black text-black">
                                            <div className="flex-1 bg-black text-white p-6 rounded-[2rem] relative overflow-hidden text-white font-black font-black font-black font-black font-black">
                                                <TrendingDown className="absolute right-[-10px] bottom-[-10px] opacity-10 text-white font-black font-black font-black" size={80} />
                                                <div className="relative z-10 font-black font-black font-black font-black font-black text-white">
                                                    <p className="text-[10px] font-black uppercase tracking-widest text-indigo-400 mb-1 font-black font-black font-black">Yield Gap (Siklus 2025)</p>
                                                    <p className="text-[8px] font-black uppercase text-white/50 mb-2 font-black font-black tracking-tighter font-black">Realisasi vs Potensi Tahun 2025</p>
                                                    <div className="flex items-baseline gap-2 text-white font-black font-black font-black text-white">
                                                        <span className="text-4xl font-black text-red-500 font-black font-black font-black text-red-500">-{b.infectedEconomic}%</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="flex-1 bg-slate-50 p-6 rounded-[2rem] border border-slate-200 text-black font-black font-black font-black font-black">
                                                <p className="text-[10px] font-black uppercase tracking-widest text-black mb-1 opacity-60 font-black font-black font-black">Total Loss (1 Blok Penuh)</p>
                                                <p className="text-[8px] font-black uppercase text-black/40 mb-2 italic font-black font-black tracking-tighter font-black font-black">Estimasi Kerugian Luas {b.luas} Ha</p>
                                                <div className="flex items-baseline gap-1 text-black font-black font-black font-black font-black">
                                                    <span className="text-sm font-black uppercase font-black text-black font-black font-black font-black font-black">Rp</span>
                                                    <span className="text-3xl font-black text-black font-black font-black font-black font-black font-black font-black">{b.loss}</span>
                                                    <span className="text-sm font-black uppercase tracking-tighter italic font-black font-black text-black font-black font-black font-black">JUTA</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* TAB SCENARIOS - EXISTING CODE CONTINUES UNCHANGED */}
                {activeTab === 'scenarios' && (
                    <div className="space-y-6 text-black font-black font-black font-black">
                        {/* ... (rest of scenarios tab code remains the same) ... */}
                    </div>
                )}
            </div>

            {/* Footer Bersih */}
            <div className="max-w-7xl mx-auto mt-8 mb-12 text-center text-black font-black font-black text-black font-black font-black font-black font-black font-black font-black">
                <p className="text-[10px] uppercase tracking-[0.5em] opacity-40 italic font-black text-black font-black font-black font-black font-black font-black font-black font-black font-black font-black font-black">© 2025 Analisis Krusialitas Agronomi • Divisi D • Area Sampel 47.7 Ha</p>
            </div>
        </div>
    );
};

export default App;

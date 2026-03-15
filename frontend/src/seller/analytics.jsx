import { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import NavBar from '../reusableComponents/navBar';
import { getData } from '../reusableComponents/api.jsx';
import './analytics.css';

// toggle to false when backend endpoints are ready
const USE_MOCK_DATA = true;

// local mock data
const MOCK_DATA = {
    stats: {
        listings: 142,
        reservations: 97,
        revenue: 2436.50,
        collectionRate: 84.0,
        noShows: 11,
    },
    wasteProxy: {
        bundles_collected: 81,
        kg_saved: 48.6,
        assumed_weight_kg_per_bundle: 0.6,
    },
    sellThrough: {
        collected: 81,
        no_show: 11,
        expired: 3,
        reserved: 2,
        total: 97,
        sell_through_rate: 83.5,
    },
    categories: [
        { category: 'Bakery', total_reservations: 34 },
        { category: 'Deli', total_reservations: 22 },
        { category: 'Produce', total_reservations: 18 },
        { category: 'Dairy', total_reservations: 14 },
        { category: 'Hot Food', total_reservations: 9 },
    ],
    pickupWindows: [
        { pickup_window: '08:00–10:00', total_reservations: 28 },
        { pickup_window: '12:00–14:00', total_reservations: 35 },
        { pickup_window: '17:00–19:00', total_reservations: 22 },
        { pickup_window: '19:00–21:00', total_reservations: 12 },
    ],
    pricing: [
        { price_range: '£0-£3', total_reservations: 18, collected: 12, sell_through_rate: 66.7 },
        { price_range: '£3-£6', total_reservations: 41, collected: 36, sell_through_rate: 87.8 },
        { price_range: '£6-£10', total_reservations: 27, collected: 24, sell_through_rate: 88.9 },
        { price_range: '£10+', total_reservations: 11, collected: 9, sell_through_rate: 81.8 },
    ],
};

function StatTile({ label, value, icon, sub, accent }) {
    return (
        <div className={`tile-card${accent ? ' tile-card--accent' : ''}`}>
            <div className="tile-icon">{icon}</div>
            <div className="tile-body">
                <span className="tile-value">{value ?? '—'}</span>
                <span className="tile-label">{label}</span>
                {sub && <span className="tile-sub">{sub}</span>}
            </div>
        </div>
    );
}

function ChartCard({ title, children, wide }) {
    return (
        <div className={`chart-card${wide ? ' chart-card--wide' : ''}`}>
            <h3 className="chart-title">{title}</h3>
            {children}
        </div>
    );
}

function Skeleton() {
    return <div className="skeleton" />;
}

function Analytics() {
    const sellerId = localStorage.getItem("seller_id") || localStorage.getItem("sellerId") || "1";

    const [stats, setStats] = useState(null);
    const [wasteProxy, setWasteProxy] = useState(null);
    const [sellThrough, setSellThrough] = useState(null);
    const [categories, setCategories] = useState(null);
    const [pickupWindows, setPickupWindows] = useState(null);
    const [pricing, setPricing] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setError(null);
        setLoading(true);

        if (USE_MOCK_DATA) {
            setStats(MOCK_DATA.stats);
            setWasteProxy(MOCK_DATA.wasteProxy);
            setSellThrough(MOCK_DATA.sellThrough);
            setCategories(MOCK_DATA.categories);
            setPickupWindows(MOCK_DATA.pickupWindows);
            setPricing(MOCK_DATA.pricing);
            setLoading(false);
            return;
        }

        const params = { seller_id: sellerId };

        async function fetchAll() {
            try {
                const [
                    listings,
                    reservations,
                    revenue,
                    collectionRate,
                    noShows,
                    sellThroughData,
                    categoriesData,
                    pickupData,
                    pricingData,
                    wasteProxyData,
                    // authenticate: false
                    // analytics endpoints are public at the moment, so skip the token
                    // this helps avoid 401s from stale local auth during development
                ] = await Promise.all([
                    getData('analytics/total-listings/', params, false),
                    getData('analytics/total-reservations/', params, false),
                    getData('analytics/total-revenue/', params, false),
                    getData('analytics/food-waste-reduction/', params, false),
                    getData('analytics/total-no-shows/', params, false),
                    getData('analytics/sell-through/', params, false),
                    getData('analytics/popular-categories/', params, false),
                    getData('analytics/best-pickup-windows/', params, false),
                    getData('analytics/pricing-effectiveness/', params, false),
                    getData('analytics/waste-proxy/', params, false),
                ]);

                // getData() returns undefined on network errors / backend unreachable
                if (listings === undefined && reservations === undefined) {
                    setError(`Could not reach the backend (seller_id: ${sellerId}). Check the server is running.`);
                    return;
                }

                setStats({
                    listings: typeof listings === 'number' ? listings : listings?.count ?? null,
                    reservations: reservations?.total_reservations ?? null,
                    revenue: typeof revenue === 'number' ? revenue : revenue?.total_revenue ?? null,
                    collectionRate: collectionRate?.food_waste_reduction_percentage ?? null,
                    noShows: noShows?.total_no_shows ?? null,
                });
                setWasteProxy(wasteProxyData ?? null);
                setSellThrough(sellThroughData);
                setCategories(Array.isArray(categoriesData) ? categoriesData : null);
                setPickupWindows(Array.isArray(pickupData) ? pickupData : null);
                setPricing(Array.isArray(pricingData) ? pricingData : null);
            } catch (err) {
                console.error('Analytics fetch error:', err);
                setError(`Unexpected error: ${err.message}`);
            } finally {
                setLoading(false);
            }
        }

        fetchAll();
    }, [sellerId]);

    const fmtRevenue = (v) =>
        v != null ? `£${Number(v).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '—';
    const fmtPct = (v) => (v != null ? `${Number(v).toFixed(1)}%` : '—');

    // shared Plotly config so all charts keep the same look/spacing
    const plotConfig = { displayModeBar: false, responsive: true };
    const plotLayout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { family: 'Inter, system-ui, sans-serif', color: '#1B2D23', size: 12 },
        margin: { t: 10, r: 16, b: 50, l: 50 },
        showlegend: false,
    };

    // sell-through donut
    const donutData = sellThrough
        ? [{
            type: 'pie',
            hole: 0.55,
            values: [
                sellThrough.collected ?? 0,
                sellThrough.no_show ?? 0,
                sellThrough.expired ?? 0,
                sellThrough.reserved ?? 0,
            ],
            labels: ['Collected', 'No-show', 'Expired', 'Reserved'],
            marker: {
                colors: ['#2D6A4F', '#E9C46A', '#E76F51', '#52B788'],
            },
            textinfo: 'percent',
            hovertemplate: '%{label}: %{value} (%{percent})<extra></extra>',
        }]
        : null;

    // popular categories
    const catData = categories && categories.length > 0
        ? [{
            type: 'bar',
            orientation: 'h',
            x: categories.map(c => c.total_reservations),
            y: categories.map(c => c.category || 'Unknown'),
            marker: { color: '#2D6A4F' },
            hovertemplate: '%{y}: %{x} reservations<extra></extra>',
        }]
        : null;

    // best pickup windows
    const pickupData = pickupWindows && pickupWindows.length > 0
        ? [{
            type: 'bar',
            x: pickupWindows.map(p => p.pickup_window || 'Unknown'),
            y: pickupWindows.map(p => p.total_reservations),
            marker: { color: '#52B788' },
            hovertemplate: '%{x}: %{y} reservations<extra></extra>',
        }]
        : null;

    // pricing effectiveness
    const pricingData = pricing && pricing.length > 0
        ? [{
            type: 'bar',
            x: pricing.map(p => p.price_range),
            y: pricing.map(p => p.sell_through_rate),
            marker: { color: '#2D6A4F' },
            hovertemplate: '%{x}: %{y}% sell-through<extra></extra>',
        }]
        : null;

    return (
        <div className="analytics-page">
            <NavBar user_type="seller" />

            <div className="analytics-container">
                <div className="analytics-header">
                    <h1 className="analytics-title">Analytics</h1>
                </div>

                {error && (
                    <div className="analytics-error">
                        <strong>Could not load data</strong>
                        <span>{error}</span>
                    </div>
                )}

                <div className="tile-grid">
                    {loading ? (
                        Array.from({ length: 6 }).map((_, i) => <div key={i} className="tile-card"><Skeleton /></div>)
                    ) : (
                        <>
                            <StatTile
                                icon="📋"
                                label="Listings Posted"
                                value={stats?.listings ?? '—'}
                                sub="all time"
                            />
                            <StatTile
                                icon="📅"
                                label="Reservations Made"
                                value={stats?.reservations ?? '—'}
                                sub="all time"
                            />
                            <StatTile
                                icon="💷"
                                label="Revenue Generated"
                                value={fmtRevenue(stats?.revenue)}
                                sub="all time"
                            />
                            <StatTile
                                icon="✅"
                                label="Collection Rate"
                                value={fmtPct(stats?.collectionRate)}
                                sub="collected / total"
                            />
                            <StatTile
                                icon="⚠️"
                                label="No-show Rate"
                                value={stats?.noShows != null && stats?.reservations
                                    ? fmtPct((stats.noShows / stats.reservations) * 100)
                                    : '—'}
                                sub="of reservations"
                            />
                            <StatTile
                                icon="🌱"
                                label="Food Waste Saved"
                                value={wasteProxy?.kg_saved != null ? `${wasteProxy.kg_saved} kg` : '—'}
                                sub={wasteProxy?.bundles_collected != null ? `${wasteProxy.bundles_collected} bundles collected` : 'all time'}
                            />
                        </>
                    )}
                </div>

                {/* ── Charts
                     current layout is split into two rows of two cards
                     keep shared visual changes in plotLayout / plotConfig so the charts stay consistent
                */}
                <div className="charts-row">
                    <ChartCard title="Reservation Outcomes">
                        {loading ? <Skeleton /> : donutData ? (
                            <Plot
                                data={donutData}
                                layout={{
                                    ...plotLayout,
                                    showlegend: true,
                                    legend: { orientation: 'h', x: 0, y: -0.15 },
                                    margin: { t: 10, r: 16, b: 60, l: 16 },
                                    annotations: [{
                                        text: sellThrough?.sell_through_rate != null
                                            ? `${Number(sellThrough.sell_through_rate).toFixed(0)}%`
                                            : '',
                                        x: 0.5, y: 0.5,
                                        font: { size: 22, color: '#1B2D23', weight: 'bold' },
                                        showarrow: false,
                                    }],
                                }}
                                config={plotConfig}
                                style={{ width: '100%', height: '280px' }}
                            />
                        ) : <p className="no-data">No outcome data available.</p>}
                    </ChartCard>

                    <ChartCard title="Popular Categories">
                        {loading ? <Skeleton /> : catData ? (
                            <Plot
                                data={catData}
                                layout={{
                                    ...plotLayout,
                                    xaxis: { title: 'Reservations', gridcolor: '#E8F0EA' },
                                    yaxis: { automargin: true },
                                    margin: { t: 10, r: 16, b: 50, l: 120 },
                                }}
                                config={plotConfig}
                                style={{ width: '100%', height: '280px' }}
                            />
                        ) : <p className="no-data">No category data available.</p>}
                    </ChartCard>
                </div>

                <div className="charts-row">
                    <ChartCard title="Best Pickup Windows">
                        {loading ? <Skeleton /> : pickupData ? (
                            <Plot
                                data={pickupData}
                                layout={{
                                    ...plotLayout,
                                    xaxis: { title: 'Pickup Window', automargin: true },
                                    yaxis: { title: 'Reservations', gridcolor: '#E8F0EA' },
                                }}
                                config={plotConfig}
                                style={{ width: '100%', height: '280px' }}
                            />
                        ) : <p className="no-data">No pickup window data available.</p>}
                    </ChartCard>

                    <ChartCard title="Sell-through by Price Range">
                        {loading ? <Skeleton /> : pricingData ? (
                            <Plot
                                data={pricingData}
                                layout={{
                                    ...plotLayout,
                                    xaxis: { title: 'Price Range' },
                                    yaxis: { title: 'Sell-through %', range: [0, 100], gridcolor: '#E8F0EA' },
                                }}
                                config={plotConfig}
                                style={{ width: '100%', height: '280px' }}
                            />
                        ) : <p className="no-data">No pricing data available.</p>}
                    </ChartCard>
                </div>

            </div>
        </div>
    );
}

export default Analytics;
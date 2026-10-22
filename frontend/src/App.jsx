import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import BeyonderDirectory from './components/BeyonderDirectory';
import PotionCodex from './components/PotionCodex';
import CommissionBoard from './components/CommissionBoard';
import ClaimsList from './components/ClaimsList';
import SquadFormation from './components/SquadFormation';
import DispatchModal from './components/DispatchModal';
import DebriefModal from './components/DebriefModal';
import BeyonderFormModal from './components/BeyonderFormModal';
import CommissionFormModal from './components/CommissionFormModal';

import {
  getPathways,
  getBeyonders,
  createBeyonder,
  updateBeyonder,
  deleteBeyonder,
  getPotions,
  getCommissions,
  createCommission,
  deleteCommission,
  claimCommission,
  getClaims,
  postDebrief,
  getMetrics,
  getSquads,
  createSquad,
  updateSquad,
  deleteSquad,
  dispatchSquad,
} from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  // Core state
  const [pathways, setPathways] = useState([]);
  const [beyonders, setBeyonders] = useState([]);
  const [potions, setPotions] = useState([]);
  const [commissions, setCommissions] = useState([]);
  const [claims, setClaims] = useState([]);
  const [squads, setSquads] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [loading, setLoading] = useState(true);

  // Modal State
  const [isDispatchModalOpen, setIsDispatchModalOpen] = useState(false);
  const [selectedCommissionForDispatch, setSelectedCommissionForDispatch] = useState(null);

  const [isDebriefModalOpen, setIsDebriefModalOpen] = useState(false);
  const [selectedClaimForDebrief, setSelectedClaimForDebrief] = useState(null);

  const [isBeyonderModalOpen, setIsBeyonderModalOpen] = useState(false);
  const [editingBeyonder, setEditingBeyonder] = useState(null);

  const [isCommissionModalOpen, setIsCommissionModalOpen] = useState(false);

  // Load all initial data from backend
  const refreshAllData = async () => {
    try {
      const [pathwaysData, beyondersData, potionsData, commissionsData, claimsData, metricsData, squadsData] =
        await Promise.all([
          getPathways(),
          getBeyonders(),
          getPotions(),
          getCommissions(),
          getClaims(),
          getMetrics(),
          getSquads(),
        ]);

      setPathways(pathwaysData);
      setBeyonders(beyondersData);
      setPotions(potionsData);
      setCommissions(commissionsData);
      setClaims(claimsData);
      setMetrics(metricsData);
      setSquads(squadsData);
    } catch (err) {
      console.error('Failed to load data from FastAPI backend:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshAllData();
  }, []);

  // Handlers
  const handleOpenDispatch = (commission = null) => {
    setSelectedCommissionForDispatch(commission);
    setIsDispatchModalOpen(true);
  };

  const handleOpenDebrief = (claim) => {
    setSelectedClaimForDebrief(claim);
    setIsDebriefModalOpen(true);
  };

  const handleOpenAddBeyonder = () => {
    setEditingBeyonder(null);
    setIsBeyonderModalOpen(true);
  };

  const handleOpenEditBeyonder = (agent) => {
    setEditingBeyonder(agent);
    setIsBeyonderModalOpen(true);
  };

  const handleBeyonderSubmit = async (data) => {
    if (editingBeyonder) {
      await updateBeyonder(editingBeyonder.id, data);
    } else {
      await createBeyonder(data);
    }
    await refreshAllData();
  };

  const handleDeleteBeyonder = async (id) => {
    if (window.confirm('Decommission this Beyonder operative?')) {
      await deleteBeyonder(id);
      await refreshAllData();
    }
  };

  const handleCommissionSubmit = async (data) => {
    await createCommission(data);
    await refreshAllData();
  };

  const handleDeleteCommission = async (id) => {
    if (window.confirm('Remove this commission from the board?')) {
      await deleteCommission(id);
      await refreshAllData();
    }
  };

  const handleDispatchSubmit = async (commissionId, beyonderId) => {
    await claimCommission(commissionId, beyonderId);
    await refreshAllData();
  };

  const handleDebriefSubmit = async (claimId, data) => {
    await postDebrief(claimId, data);
    await refreshAllData();
  };

  // Squad handlers
  const handleCreateSquad = async (data) => {
    await createSquad(data);
    await refreshAllData();
  };

  const handleUpdateSquad = async (id, data) => {
    await updateSquad(id, data);
    await refreshAllData();
  };

  const handleDeleteSquad = async (id) => {
    if (window.confirm('Disband this squad? This action cannot be undone.')) {
      await deleteSquad(id);
      await refreshAllData();
    }
  };

  const handleDispatchSquad = async (squadId, commissionId) => {
    await dispatchSquad(squadId, commissionId);
    await refreshAllData();
  };

  return (
    <div className="min-h-screen bg-[#0a0b0e] text-slate-100 flex flex-col font-serif">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} squadCount={squads.length} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="w-12 h-12 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin"></div>
            <p className="text-[#e6c656] font-serif text-sm gold-glow">
              Connecting to Tarot Command Center Database...
            </p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <Dashboard
                metrics={metrics}
                commissions={commissions}
                beyonders={beyonders}
                onOpenDispatch={handleOpenDispatch}
                setActiveTab={setActiveTab}
              />
            )}

            {activeTab === 'beyonders' && (
              <BeyonderDirectory
                beyonders={beyonders}
                pathways={pathways}
                onOpenAddModal={handleOpenAddBeyonder}
                onOpenEditModal={handleOpenEditBeyonder}
                onDeleteBeyonder={handleDeleteBeyonder}
              />
            )}

            {activeTab === 'potions' && (
              <PotionCodex potions={potions} pathways={pathways} />
            )}

            {activeTab === 'commissions' && (
              <CommissionBoard
                commissions={commissions}
                onOpenAddModal={() => setIsCommissionModalOpen(true)}
                onOpenDispatchModal={handleOpenDispatch}
                onDeleteCommission={handleDeleteCommission}
              />
            )}

            {activeTab === 'claims' && (
              <ClaimsList
                claims={claims}
                onOpenDebriefModal={handleOpenDebrief}
                onOpenDispatchModal={handleOpenDispatch}
              />
            )}

            {activeTab === 'squads' && (
              <SquadFormation
                squads={squads}
                beyonders={beyonders}
                commissions={commissions}
                onCreateSquad={handleCreateSquad}
                onUpdateSquad={handleUpdateSquad}
                onDeleteSquad={handleDeleteSquad}
                onDispatchSquad={handleDispatchSquad}
              />
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-[#c5a059]/20 bg-[#0c0e14] py-4 text-center text-xs text-slate-500 font-serif">
        <p>Lord of the Mysteries • Tarot Administrative System • Praise The Fool 🎴</p>
      </footer>

      {/* Modals */}
      <DispatchModal
        isOpen={isDispatchModalOpen}
        onClose={() => setIsDispatchModalOpen(false)}
        commissions={commissions}
        beyonders={beyonders}
        preselectedCommission={selectedCommissionForDispatch}
        onDispatchSuccess={handleDispatchSubmit}
      />

      <DebriefModal
        isOpen={isDebriefModalOpen}
        onClose={() => setIsDebriefModalOpen(false)}
        claim={selectedClaimForDebrief}
        onDebriefSubmit={handleDebriefSubmit}
      />

      <BeyonderFormModal
        isOpen={isBeyonderModalOpen}
        onClose={() => setIsBeyonderModalOpen(false)}
        pathways={pathways}
        editingBeyonder={editingBeyonder}
        onSubmit={handleBeyonderSubmit}
      />

      <CommissionFormModal
        isOpen={isCommissionModalOpen}
        onClose={() => setIsCommissionModalOpen(false)}
        onSubmit={handleCommissionSubmit}
      />
    </div>
  );
}

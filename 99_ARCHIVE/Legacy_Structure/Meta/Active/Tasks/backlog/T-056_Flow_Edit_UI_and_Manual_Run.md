# Task ID: T-056

- **Source Document:** Field UX Gap
- **Title:** Flow Edit UI & Manual Run Controls
- **Description:**
  OluŸturulmuŸ flow'larn ad/a‡klamas/config'i dzenlenemiyor ve manuel ‡alŸtrma i‡in net UI yok. Flow yönetimine edit ve manuel run kontrolleri eklenmeli.

  **Yaplacaklar:**
  1. Flow listesinde "Edit" modal/form (name, description, is_active, trigger config) ekle
  2. Manuel run butonunu daha belirgin ve ‡alŸma durumunu g”steren state ekle
  3. Update API/useFlows updateFlow entegrasyonunu test et
  4. Edit/rerun i‡in unit/component testleri ekle

  **Acceptance Criteria:**
  - [ ] Flow ad/a‡klamas UI'dan dzenlenebiliyor ve kaydediliyor
  - [ ] Manuel run butonu net, loading state g”steriyor, ‡ikt üretiyor
  - [ ] Edit/run i‡in testler ge‡iyor

- **Priority:** P2 (UX/Functionality)
- **Assigned To:** @Delegate (Çırak)
- **Complexity:** Medium
- **Estimated Effort:** 2-3 hours
- **Dependencies:** useFlows.updateFlow, FlowEngine run

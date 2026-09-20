"use strict";

import { installPollingGovernor } from "./core/polling-governor.js";
import { initI18n } from "./core/i18n.js?v=i18n-fix-20260920b";
import { initStatusBar } from "./components/status-bar.js";
import { initNotificationCenter } from "./components/notification-center.js";
import { initPanelHelp } from "./components/help.js";
import { initRuntimeIO } from "./modules/runtime-io.js";
import { initScienceTransparency } from "./modules/science-transparency.js";
import { initScientificMetrics } from "./modules/scientific-metrics.js";
import { initExperimentLab } from "./modules/experiment-lab.js";
import { initFunctionalCompletion } from "./modules/functional-completion.js";
import { initIntegratedNervousSystem } from "./modules/integrated-nervous-system.js";
import { startDataStyleObserver } from "./modules/data-styles.js";
import { initCognition } from "./modules/cognition.js";
import { initGatewayMonitor } from "./modules/gateway-monitor.js";
import { initDocsBrowser } from "./modules/docs-browser.js";
import { initResearchDocs } from "./modules/research-docs.js";
import { initAIReportTools } from "./modules/ai-report-tools.js";
import { initLearningPrep } from "./modules/learning-prep.js";
import { initStructuralInspector } from "./modules/structural-inspector.js";
import { initSystemInfo } from "./modules/system-info.js";
import { initSnapshotHistory } from "./modules/snapshot-history.js";
import { initReviewLink } from "./modules/review-link.js";
import { initOverviewSubtabs } from "./modules/overview-subtabs.js";
import { initPublicationPanel } from "./modules/publication-reader.js";
import { initPublicationScholarTools } from "./modules/publication-scholar-bootstrap.js";
import { initPublicationReaderPolish } from "./modules/publication-reader-polish.js";
import { initPublicationImprint } from "./modules/publication-imprint.js";
import { initPublicationExplainer } from "./modules/publication-explainer.js";
import { initResearchSubtabs } from "./modules/research-subtabs.js";
import { initNeuronModelScience } from "./modules/neuron-model-science.js";
import { initRuntimeNeuron } from "./modules/runtime-neuron.js";
import { initSmallSNNStage } from "./modules/small-snn-stage.js";
import { initRecurrentSNNStage } from "./modules/recurrent-snn-stage.js";
import { initWorkspaceRouter } from "./workspace-router.js";
import { initExternalReview } from "../external-review.js";

installPollingGovernor();

function init() {
  initI18n();
  initWorkspaceRouter();
  // The legacy bootstrap may have created this panel before its mount existed.
  // Idempotent reattachment keeps the original listeners and metadata request.
  initExternalReview();
  initStatusBar();
  initNotificationCenter();
  initPanelHelp();
  initRuntimeIO();
  initScienceTransparency();
  initScientificMetrics();
  initExperimentLab();
  initFunctionalCompletion();
  initIntegratedNervousSystem();
  startDataStyleObserver();
  initCognition();
  initGatewayMonitor();
  initDocsBrowser();
  initResearchDocs();
  initAIReportTools();
  initLearningPrep();
  initStructuralInspector();
  initSystemInfo();
  initSnapshotHistory();
  initReviewLink();
  initOverviewSubtabs();
  initPublicationPanel();
  initPublicationScholarTools();
  initPublicationReaderPolish();
  initPublicationImprint();
  initPublicationExplainer();
  initResearchSubtabs();
  initNeuronModelScience();
  initRuntimeNeuron();
  initSmallSNNStage();
  initRecurrentSNNStage();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => setTimeout(init, 0), { once: true });
} else {
  setTimeout(init, 0);
}

window.MHRNFrontend = { refresh: init };

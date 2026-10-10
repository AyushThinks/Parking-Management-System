# Viva Preparation — Questions and Short Answers

1. **What is the objective?** To manage vehicle entry/exit, parking slots, fees and records while applying TQM tools to improve quality.
2. **What is TQM?** Total Quality Management is an organization-wide approach focused on customer satisfaction, process quality and continuous improvement.
3. **What is Poka-Yoke?** Error-proofing. This project validates inputs and blocks duplicate active vehicle entries before saving.
4. **What is FMEA?** Failure Mode and Effects Analysis identifies possible failures, their effects and controls.
5. **How is RPN calculated?** Severity × Occurrence × Detection difficulty. A higher RPN indicates a higher priority for investigation.
6. **What is SIPOC?** A high-level map of Suppliers, Inputs, Process, Outputs and Customers.
7. **What is CTQ?** Critical to Quality: measurable product/process characteristics tied to customer needs.
8. **What does Pareto analysis show?** It ranks defect categories by frequency to identify the largest contributors.
9. **What does a Fishbone diagram do?** It organizes possible root causes into categories for investigation; it does not prove a cause by itself.
10. **Explain PDCA.** Plan a change, Do it, Check evidence, Act by standardizing or revising.
11. **Why SQLite?** It is lightweight, local and does not require a separate database server.
12. **Why separate service and UI?** Business rules can be tested without opening the GUI and are easier to maintain.
13. **How is parking fee calculated?** Any started hour is billed as a full hour, minimum one hour, multiplied by the configured rate.
14. **How do you prevent two vehicles using the same slot?** The service allocates an available slot and a partial unique index protects active slot uniqueness.
15. **What are project limitations?** It does not connect to real gates, payment systems, cameras or cloud multi-user services.
16. **What is continuous improvement evidence?** Dated defects, test results, corrective actions and re-test results, not assumptions alone.

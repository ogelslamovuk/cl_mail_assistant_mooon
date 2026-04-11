from src.pipeline.case_thread_binding.module import CaseThreadBindingModule
from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.identity_context_enrichment.module import IdentityContextEnrichmentModule
from src.pipeline.knowledge_rag.module import KnowledgeRagModule
from src.pipeline.llm_understanding.module import LlmUnderstandingModule
from src.pipeline.mail_import.module import MailImportModule
from src.pipeline.operator_actions.module import OperatorActionsModule
from src.pipeline.pre_triage.module import PreTriageModule
from src.pipeline.reply_sender.module import ReplySenderModule
from src.pipeline.router.module import RouterModule
from src.pipeline.telegram_operator_delivery.module import TelegramOperatorDeliveryModule

PIPELINE_ORDER = [
    "mail_import",
    "pre_triage",
    "identity_context_enrichment",
    "case_thread_binding",
    "llm_understanding",
    "router",
    "knowledge_rag",
    "draft_builder",
    "telegram_operator_delivery",
    "operator_actions",
    "reply_sender",
]

MODULE_REGISTRY = {
    "mail_import": MailImportModule,
    "pre_triage": PreTriageModule,
    "identity_context_enrichment": IdentityContextEnrichmentModule,
    "case_thread_binding": CaseThreadBindingModule,
    "llm_understanding": LlmUnderstandingModule,
    "router": RouterModule,
    "knowledge_rag": KnowledgeRagModule,
    "draft_builder": DraftBuilderModule,
    "telegram_operator_delivery": TelegramOperatorDeliveryModule,
    "operator_actions": OperatorActionsModule,
    "reply_sender": ReplySenderModule,
}

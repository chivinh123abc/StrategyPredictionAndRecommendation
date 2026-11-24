# Project-maintained verification, separate from SpecKit installer-managed files.
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/common.ps1"
$knowledgeRepo = Get-RepoRoot
foreach ($knowledgeTemplate in @('spec-template','plan-template','tasks-template','checklist-template')) {
    $knowledgeContent = Resolve-TemplateContent -TemplateName $knowledgeTemplate -RepoRoot $knowledgeRepo
    if ([string]::IsNullOrEmpty($knowledgeContent)) { throw "Empty resolved template: $knowledgeTemplate" }
    if (-not $knowledgeContent.Contains('AI/KNOWLEDGE_RULES.md')) { throw "Missing knowledge policy: $knowledgeTemplate" }
    if (-not $knowledgeContent.Contains('TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md')) { throw "Missing register: $knowledgeTemplate" }
    $knowledgeOverride = Join-Path $knowledgeRepo ".specify/templates/overrides/$knowledgeTemplate.md"
    if ($knowledgeContent -cne [System.IO.File]::ReadAllText($knowledgeOverride,[System.Text.Encoding]::UTF8)) {
        throw "Resolver did not use project override: $knowledgeTemplate"
    }
    Write-Output "$knowledgeTemplate : project override PASS"
}

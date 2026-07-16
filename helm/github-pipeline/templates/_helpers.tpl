{{/*
Expand the name of the chart.
*/}}
{{- define "github-pipeline.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "github-pipeline.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart label.
*/}}
{{- define "github-pipeline.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "github-pipeline.labels" -}}
helm.sh/chart: {{ include "github-pipeline.chart" . }}
app.kubernetes.io/name: {{ include "github-pipeline.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "github-pipeline.selectorLabels" -}}
app.kubernetes.io/name: {{ include "github-pipeline.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
PostgreSQL service name (Bitnami subchart).
*/}}
{{- define "github-pipeline.postgresHost" -}}
{{- printf "%s-postgresql" .Release.Name }}
{{- end }}

{{/*
Full DATABASE_URL.
*/}}
{{- define "github-pipeline.databaseUrl" -}}
{{- printf "postgresql://postgres:%s@%s:5432/github_pipeline" .Values.secrets.databasePassword (include "github-pipeline.postgresHost" .) }}
{{- end }}

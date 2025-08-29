{{/*
Expand the name of the chart.
*/}}
{{- define "demo-apps.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "demo-apps.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "demo-apps.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "demo-apps.labels" -}}
helm.sh/chart: {{ include "demo-apps.chart" . }}
{{ include "demo-apps.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "demo-apps.selectorLabels" -}}
app.kubernetes.io/name: {{ include "demo-apps.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Component labels
*/}}
{{- define "demo-apps.componentLabels" -}}
{{- $component := . -}}
app.kubernetes.io/component: {{ $component }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "demo-apps.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "demo-apps.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Image name helper
*/}}
{{- define "demo-apps.image" -}}
{{- $root := .root -}}
{{- $image := .image -}}
{{- $registry := $root.Values.global.registry -}}
{{- $repository := $image.repository -}}
{{- $tag := $image.tag | default $root.Values.global.imageTag -}}
{{- if $registry -}}
{{- printf "%s/%s:%s" $registry $repository $tag -}}
{{- else -}}
{{- printf "%s:%s" $repository $tag -}}
{{- end -}}
{{- end }}

{{/*
Environment helper
*/}}
{{- define "demo-apps.environment" -}}
{{- .Values.global.environment | default "dev" -}}
{{- end }}

{{/*
Region helper
*/}}
{{- define "demo-apps.region" -}}
{{- .Values.global.region | default "eastus" -}}
{{- end }}

{{/*
Networking validation helper
*/}}
{{- define "demo-apps.validateNetworking" -}}
{{- if and .Values.ingress.enabled .Values.gateway.enabled -}}
{{- fail "ERROR: Both Ingress and Gateway API are enabled. Please enable only one networking option." -}}
{{- end -}}
{{- if and (not .Values.ingress.enabled) (not .Values.gateway.enabled) -}}
{{- fail "ERROR: Neither Ingress nor Gateway API is enabled. Please enable one networking option." -}}
{{- end -}}
{{- end }}

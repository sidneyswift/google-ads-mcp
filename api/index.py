# Copyright 2026 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Vercel serverless entrypoint for the Google Ads MCP server.

Vercel's Python runtime looks for a top-level ``app`` variable in this file
and serves it as an ASGI application. Instead of calling ``mcp.run()`` (which
starts its own long-lived web server, something serverless platforms don't
allow), we ask FastMCP for the underlying ASGI app and let Vercel serve it.

``stateless_http=True`` is required on serverless: each request can land on a
fresh instance, so the server cannot rely on in-memory session state between
requests.
"""

import os
import sys

# The `ads_mcp` package lives at the repository root (one level above this
# file), so make sure Python can find it when Vercel runs this function.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ads_mcp.coordinator import mcp

# Importing these modules registers the MCP resources on the `mcp` singleton
# (same pattern as ads_mcp/server.py). Tools are mounted by coordinator.py.
from ads_mcp.resources import (
    discovery,
    metrics,
    release_notes,
    segments,
)  # noqa: F401

# The MCP endpoint is served at /mcp (FastMCP's default path).
app = mcp.http_app(stateless_http=True)

import { makeApi, Zodios, type ZodiosOptions } from "@zodios/core";
import { z } from "zod";

const PostUserBody = z.object({ user_name: z.string() }).passthrough();
const SelfUserRes = z
  .object({
    user_id: z.string(),
    user_name: z.string(),
    user_screen_id: z.string(),
    user_icon_uuid: z.string(),
    user_date: z.string().datetime({ offset: true }),
    user_mail: z.string(),
  })
  .passthrough();
const ValidationError = z
  .object({
    loc: z.array(z.union([z.string(), z.number()])),
    msg: z.string(),
    type: z.string(),
  })
  .passthrough();
const HTTPValidationError = z
  .object({ detail: z.array(ValidationError) })
  .partial()
  .passthrough();
const PostTokenBody = z.object({ keycloak_token: z.string() }).passthrough();
const TokenInfo = z
  .object({ token: z.string(), expire: z.string().datetime({ offset: true }) })
  .passthrough();
const TokenRes = z
  .object({ access: TokenInfo, refresh: TokenInfo })
  .passthrough();
const q = z.union([z.array(z.string()), z.null()]).optional();
const post_by = z.union([z.array(z.string().uuid()), z.null()]).optional();
const start_datetime = z.union([z.string(), z.null()]).optional();
const following = z.union([z.boolean(), z.null()]).optional();
const read_limit_number = z.union([z.number(), z.null()]).optional();

export const schemas = {
  PostUserBody,
  SelfUserRes,
  ValidationError,
  HTTPValidationError,
  PostTokenBody,
  TokenInfo,
  TokenRes,
  q,
  post_by,
  start_datetime,
  following,
  read_limit_number,
};

const endpoints = makeApi([
  {
    method: "post",
    path: "/api/token",
    alias: "post_token_api_token_post",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: z.object({ keycloak_token: z.string() }).passthrough(),
      },
    ],
    response: TokenRes,
    errors: [
      {
        status: 422,
        description: `Validation Error`,
        schema: HTTPValidationError,
      },
    ],
  },
  {
    method: "post",
    path: "/api/user",
    alias: "post_user_api_user_post",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: z.object({ user_name: z.string() }).passthrough(),
      },
    ],
    response: SelfUserRes,
    errors: [
      {
        status: 422,
        description: `Validation Error`,
        schema: HTTPValidationError,
      },
    ],
  },
  {
    method: "get",
    path: "/api/user/self",
    alias: "get_user_api_user_self_get",
    requestFormat: "json",
    response: SelfUserRes,
  },
  {
    method: "get",
    path: "/health",
    alias: "health_health_get",
    requestFormat: "json",
    response: z.unknown(),
  },
  {
    method: "get",
    path: "/products/",
    alias: "read_products_products__get",
    requestFormat: "json",
    parameters: [
      {
        name: "q",
        type: "Query",
        schema: q,
      },
      {
        name: "post_by",
        type: "Query",
        schema: post_by,
      },
      {
        name: "start_datetime",
        type: "Query",
        schema: start_datetime,
      },
      {
        name: "end_datetime",
        type: "Query",
        schema: start_datetime,
      },
      {
        name: "following",
        type: "Query",
        schema: following,
      },
      {
        name: "read_limit_number",
        type: "Query",
        schema: read_limit_number,
      },
    ],
    response: z.unknown(),
    errors: [
      {
        status: 422,
        description: `Validation Error`,
        schema: HTTPValidationError,
      },
    ],
  },
]);

export const api = new Zodios(endpoints);

export function createApiClient(baseUrl: string, options?: ZodiosOptions) {
  return new Zodios(baseUrl, endpoints, options);
}

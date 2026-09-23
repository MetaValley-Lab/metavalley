export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  user: {
    id: string;
    email: string;
  };
}

export interface RegisterResponse {
  message: string;
  user: {
    id: string;
    email: string;
  };
}


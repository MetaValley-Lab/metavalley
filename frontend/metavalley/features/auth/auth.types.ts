export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  message: string;
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


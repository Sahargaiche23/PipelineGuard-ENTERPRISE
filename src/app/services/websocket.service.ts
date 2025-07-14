import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class WebsocketService {
  private ws: WebSocket | null = null;
  private notifications: any[] = [];
  public notifications$: Subject<any> = new Subject();

  constructor(private auth: AuthService) {}

  connect() {
    if (!this.auth.getToken()) return;
    const token = this.auth.getToken();
    this.ws = new WebSocket(`ws://localhost:8000/ws/${token}`);

    this.ws.onmessage = (event) => {
      const notif = JSON.parse(event.data);
      if (!this.notifications.find(n => n.id === notif.id)) {
        this.notifications.push(notif);
        this.notifications$.next(notif);
      }
    };

    this.ws.onclose = () => setTimeout(() => this.connect(), 3000);
  }

  close() { this.ws?.close(); }
  getAllNotifications() { return this.notifications; }
}
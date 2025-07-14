import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private ws: WebSocket | null = null;
  private notificationsSubject = new Subject<any>();
  private reconnectInterval = 3000;
  private isConnecting = false;
  private maxReconnectAttempts = 5;
  private reconnectAttempts = 0;

  public notifications$: Observable<any> = this.notificationsSubject.asObservable();

  constructor(private authService: AuthService) {}

  connect(): void {
    if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) {
      console.log('🔄 Connexion déjà en cours ou active');
      return;
    }

    const token = this.authService.getToken();
    if (!token || token === 'undefined') {
      console.error('❌ Token manquant ou invalide. Impossible de se connecter au WebSocket.');
      return;
    }

    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Nombre maximum de tentatives de reconnexion atteint');
      return;
    }

    this.isConnecting = true;
    console.log(`🔌 Tentative de connexion WebSocket (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts}) avec token:`, token.substring(0, 20) + '...');
    
    const url = `ws://localhost:8000/ws/${token}`;
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('✅ WebSocket connecté avec succès');
      this.isConnecting = false;
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      console.log('📨 Message reçu:', event.data);
      try {
        const notif = JSON.parse(event.data);
        this.notificationsSubject.next(notif);
      } catch (error) {
        console.error('❌ Erreur parsing JSON:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('💥 WebSocket erreur:', error);
      this.isConnecting = false;
    };

    this.ws.onclose = (event) => {
      console.warn(`🔌 WebSocket fermé. Code: ${event.code}, Raison: ${event.reason || 'Aucune raison'}`);
      this.isConnecting = false;
      
      if (event.code === 1006) {
        console.error('❌ Connexion fermée anormalement - Vérifiez le backend et l\'authentification');
      }
      
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        console.warn(`🔌 Nouvelle tentative dans 3 secondes... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        setTimeout(() => this.connect(), this.reconnectInterval);
      } else {
        console.error('❌ Arrêt des tentatives de reconnexion');
      }
    };
  }

  close(): void {
    this.ws?.close();
  }

  // Méthode pour ajouter des notifications de test
  addTestNotification(): void {
    const testNotif = {
      id: Date.now(),
      title: 'Trump administration shuts down U.S. website on climate change',
      content: 'Test notification from Kafka consumer data',
      url: 'https://www.latimes.com/environment/story/2025-07-01/trump-us-climate-website',
      created_at: new Date().toISOString()
    };
    this.notificationsSubject.next(testNotif);
  }

  // Méthode pour tester la validité du token
  testToken(): void {
    const token = this.authService.getToken();
    if (token) {
      console.log('🔍 Token actuel:', token);
      try {
        // Décoder le payload du JWT (sans vérification)
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp;
        const now = Math.floor(Date.now() / 1000);
        
        console.log('📅 Token expire le:', new Date(exp * 1000));
        console.log('📅 Date actuelle:', new Date());
        console.log('⏰ Token expiré:', now > exp);
        
        if (now > exp) {
          console.error('❌ Le token a expiré! Veuillez vous reconnecter.');
        } else {
          console.log('✅ Le token est encore valide.');
        }
      } catch (error) {
        console.error('❌ Erreur lors du décodage du token:', error);
      }
    } else {
      console.error('❌ Aucun token trouvé');
    }
  }
}
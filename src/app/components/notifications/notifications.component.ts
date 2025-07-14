import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Subscription } from 'rxjs';
import { NotificationService } from 'src/app/services/notification.service';
import { HttpClient } from '@angular/common/http';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.css']
})
export class NotificationsComponent implements OnInit, OnDestroy {
  notifications: any[] = [];
  filteredNotifications: any[] = [];
  isLoading = false;
  searchTerm: string = '';
  searchResults: any[] = [];
  searching: boolean = false;
  private socketSub?: Subscription;

  constructor(
    private notificationService: NotificationService,
    private cdr: ChangeDetectorRef,
    private http: HttpClient,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const token = this.authService.getToken();
    if (!token) {
      return;
    }
    this.notificationService.connect();
    this.socketSub = this.notificationService.notifications$.subscribe({
      next: (notification) => {
        const exists = this.notifications.find(n => n.id === notification.id);
        if (!exists) {
          this.notifications.push(notification);
          this.filterNotifications();
          this.cdr.detectChanges();
        }
      },
      error: (err) => { console.error('WebSocket erreur:', err); }
    });
  }

  ngOnDestroy(): void {
    this.socketSub?.unsubscribe();
    this.notificationService.close();
  }

  clearNotifications(): void {
    const token = this.authService.getToken();
    if (!token) return;
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
    this.http.delete('http://localhost:8000/notifications', { headers }).subscribe({
      next: () => {
        this.notifications = [];
        this.filterNotifications();
        this.cdr.detectChanges();
      },
      error: () => {
        this.notifications = [];
        this.filterNotifications();
        this.cdr.detectChanges();
      }
    });
  }

  loadNotificationsFromDB(): void {
    this.isLoading = true;
    const token = this.authService.getToken();
    if (!token) {
      this.isLoading = false;
      return;
    }
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
    this.http.get<any[]>('http://localhost:8000/notifications', { headers })
      .subscribe({
        next: (data) => {
          this.isLoading = false;
          let added = 0;
          data.forEach(notif => {
            const exists = this.notifications.find(n => n.id === notif.id);
            if (!exists) {
              const formattedNotif = {
                id: notif.id,
                title: notif.title || notif.content || 'Notification Reddit',
                content: notif.content || '',
                url: notif.url || '',
                created_at: notif.created_at
              };
              this.notifications.push(formattedNotif);
              added++;
            }
          });
          this.filterNotifications();
          this.cdr.detectChanges();
        },
        error: () => {
          this.isLoading = false;
        }
      });
  }

  reconnectWebSocket(): void {
    this.notificationService.close();
    setTimeout(() => {
      this.notificationService.connect();
    }, 1000);
  }

  testToken(): void {
    this.notificationService.testToken();
  }

  trackByFn(index: number, item: any): any {
    return item.id || index;
  }

  formatDate(dateString: string): string {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      if (diffMins < 1) return 'À l\'instant';
      if (diffMins < 60) return `Il y a ${diffMins} min`;
      if (diffHours < 24) return `Il y a ${diffHours}h`;
      if (diffDays < 7) return `Il y a ${diffDays} jour${diffDays > 1 ? 's' : ''}`;
      return date.toLocaleDateString('fr-FR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      return dateString;
    }
  }

  filterNotifications(): void {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) {
      this.filteredNotifications = [...this.notifications];
      this.searchResults = [];
      this.searching = false;
      return;
    }
    this.filteredNotifications = this.notifications.filter(n =>
      (n.title && n.title.toLowerCase().includes(term)) ||
      (n.content && n.content.toLowerCase().includes(term)) ||
      (n.url && n.url.toLowerCase().includes(term))
    );
    this.searchReddit(term);
  }

  searchReddit(term: string): void {
    if (!term || term.length < 2) {
      this.searchResults = [];
      this.searching = false;
      return;
    }
    this.searching = true;
    this.http.get<any[]>(`http://localhost:8000/search?q=${encodeURIComponent(term)}`)
      .subscribe({
        next: (results) => {
          this.searchResults = results;
          this.searching = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.searchResults = [];
          this.searching = false;
        }
      });
  }
}